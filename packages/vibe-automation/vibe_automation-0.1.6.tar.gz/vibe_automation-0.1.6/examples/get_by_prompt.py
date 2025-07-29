import logging

from va import step, workflow
from va.playwright import get_browser


@workflow("Example workflow")
def main():
    with get_browser(headless=False, slow_mo=1000) as browser:
        page = browser.new_page()

        with step("navigate to the page"):
            page.goto("https://httpbin.org/forms/post")

        with step("get_by_prompt step"):
            element = page.get_by_prompt("Customer name")
            element.fill("John Done")

        with step("get_by_prompt as a fallback (not triggered)"):
            element = page.get_by_label("Telephone: ") | page.get_by_prompt("Telephone")
            element.fill("123-456-7890")

        with step("get_by_prompt as a fallback (triggered)"):
            element = page.get_by_label("Email") | page.get_by_prompt("Email address")
            element.fill("test@example.com")

        with step(
            "get_by_prompt as a fallback when the default locator throw an error"
        ):
            # Pizza Size element is there, but cannot be checked since it's not an input.
            element = page.get_by_text("Pizza Size") | page.get_by_prompt(
                "medium size pizza"
            )
            element.check()

        with step("get_by_prompt on left side of | operator"):
            # Demonstrate get_by_prompt | traditional_locator usage
            # we should trigger the get_by_text first before trying the get_by_prompt method
            element = page.get_by_prompt("Submit button") | page.get_by_text(
                "Submit order"
            )
            element.click()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
