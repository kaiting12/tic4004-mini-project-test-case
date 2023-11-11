from playwright.sync_api import sync_playwright


def login_standard_user(page):
    page.locator('[data-test="username"]').click()
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="username"]').press("Tab")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()


def login_locked_out_user(page):
    page.locator('[data-test="username"]').click()
    page.locator('[data-test="username"]').fill("locked_out_user")
    page.locator('[data-test="password"]').click()
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()


def test_standard_user_login(page):
    page.goto("https://www.saucedemo.com/")
    login_standard_user(page)

    # Assert if the login was successful and the display page URL is correct
    assert (
        page.url == "https://www.saucedemo.com/inventory.html"
    ), "Standard user login failed"


def test_locked_out_user_login(page):
    page.goto("https://www.saucedemo.com/")
    login_locked_out_user(page)

    # Assertion to check if error locator appears
    assert page.locator(
        '[data-test="error"]'
    ).is_visible(), "Locked out user login failed"


def test_adding_product_into_cart(page):
    page.goto("https://www.saucedemo.com/")
    login_standard_user(page)

    # Add 1 product to cart
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator("a").filter(has_text="1").click()

    # Assert that there is one product in the cart container
    assert (
        page.locator("#cart_contents_container").count() == 1
    ), "Cart container count is not 1"

    # Assert that there is a link with role "link" and name "Sauce Labs Backpack"
    backpack_link = page.get_by_role("link", name="Sauce Labs Backpack")
    assert backpack_link.is_visible(), "Sauce Labs Backpack link not visible"
    assert backpack_link.inner_text() == "Sauce Labs Backpack", "Unexpected inner text"

    # Assert that there is a price element with text "$29.99"
    price_element = page.get_by_text("$29.99")
    assert price_element.is_visible(), "Price $29.99 not visible"

    # Assert right product description is shown
    assert (
        page.locator(
            '//*[contains(text(), "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromis")]'
        ).count()
        == 1
    ), "Product description not found"


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        test_standard_user_login(page)
        test_locked_out_user_login(page)
        test_adding_product_into_cart(page)

        print("Everything passed")
        browser.close()
