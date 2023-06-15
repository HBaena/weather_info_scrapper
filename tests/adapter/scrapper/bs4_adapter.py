from unittest.mock import call, Mock
from mamba import before, context, describe, it

from expects import be_false, be_none, expect, equal

from src.adapters.scrapper.bs4.adapter import BS4ScrapperAdapter

with describe(BS4ScrapperAdapter) as self:
    with before.all:
        self.url = "SOME_URL"
        self.span_id = "SOME_SPAN_ID"
        self.text = "SOME_TEXT"
        self.html_body = f'<span id="{self.span_id}">{self.text}</span>'

    with before.each:
        self.scrapper = Mock()
        self.scrapper.find.return_value = Mock(text=self.text)
        self.http_client = Mock()
        self.scrapper_client = Mock()
        self.scrapper_client.return_value = self.scrapper

    with context(BS4ScrapperAdapter.get_html):
        with context("when request got a 200 response"):
            with it("should return an html body"):
                self.http_client.get.return_value = Mock(status_code=200, text=self.html_body)
                adapter = BS4ScrapperAdapter(
                    url=self.url,
                    http_client=self.http_client,
                    scrapper_client=self.scrapper_client
                )

                response = adapter.get_html()

                expect(self.http_client.get.call_args).to(equal(call(self.url)))
                expect(self.scrapper_client.call_args).to(equal(call(self.html_body, features='html.parser')))  # noqa
                expect(adapter.scrapper).to(equal(self.scrapper))
                expect(response).to(equal(self.html_body))

        with context("when request got an error"):
            with it("should return None"):
                http_request = Mock()
                self.http_client.get.return_value = Mock(
                    status_code=400,
                    text=self.html_body,
                    request=http_request,
                )
                adapter = BS4ScrapperAdapter(
                    url=self.url,
                    http_client=self.http_client,
                    scrapper_client=self.scrapper_client
                )
                response = adapter.get_html()

                expect(self.http_client.get.call_args).to(equal(call(self.url)))
                expect(self.scrapper_client.called).to(be_false)
                expect(adapter.http_request).to(equal(http_request))
                expect(response).to(be_none)

    with context(BS4ScrapperAdapter.get_text_by_span_id):
        with context("when span id exists"):
            with it("should return a text"):
                adapter = BS4ScrapperAdapter(
                    html_body=self.html_body,
                    scrapper_client=self.scrapper_client,
                )

                response = adapter.get_text_by_span_id(span_id=self.span_id)

                expect(self.scrapper_client.call_args).to(equal(call(self.html_body, features='html.parser')))  # noqa
                expect(self.scrapper.find.call_args).to(equal(call('span', id=self.span_id)))
                expect(response).to(equal(self.text))
