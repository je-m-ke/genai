#experimented to open puma and look for a product and click the firsr product, achieved only till the search =8Nov17:30

from playwright.sync_api import sync_playwright
import time

# Debug helpers
def save_debug(page, tag):
    ts = int(time.time())
    try:
        page.screenshot(path=f"debug_{tag}_{ts}.png", full_page=True)
    except Exception:
        pass
    try:
        with open(f"debug_{tag}_{ts}.html", "w", encoding="utf-8") as f:
            f.write(page.content())
    except Exception:
        pass

def click_when_visible(page, selector, description="", timeout=8000):
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.locator(selector).first.click()
        print(description + " - success")
        return True
    except Exception as e:
        print(description + " - failed:", str(e))
        return False

def open_search_and_wait(page, timeout_seconds=20):
    candidates = [
        "xpath=/html/body/div[2]/div[1]/div[1]/nav/div/div[2]/div[1]/button[1]",
        "xpath=//*[@id='nav-bar-sticky']/nav/div/div[2]/div[1]/button[1]",
        "xpath=//*[@id='puma-skip-here']/div/section/nav[1]/div/div/div/div[1]/div[2]/ul/li[4]/div/button",
        "#nav-bar-sticky > nav > div > div.flex.items-center.justify-end.gap-2.w-72 > div:nth-child(1) > button.group.tw-wiulm1.tw-ozwx86.flex-row",
        "button:has-text('SEARCH')",
        "button:has-text('Search')",
        "button[aria-label='Search']",
        "button[class*='search']",
        "button:has(svg)"
    ]
    input_selector = "input[placeholder*='Search'], input[type='search'], input[id*='search']"
    start = time.time()
    last_clicked = None

    while time.time() - start < timeout_seconds:
        for cand in candidates:
            try:
                page.wait_for_selector(cand, timeout=1200)
                page.locator(cand).first.click()
                last_clicked = cand
                try:
                    page.wait_for_selector(input_selector, timeout=2000)
                    print("Search panel open - success (clicked: " + cand + ")")
                    return True
                except Exception:
                    # Input not yet visible, try next candidate
                    continue
            except Exception:
                continue
        time.sleep(0.5)

    print("Search panel open - failed. Last clicked:", last_clicked)
    save_debug(page, "search_open_timeout")
    return False

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            # Step 1: navigate to Puma India
            page.goto("https://in.puma.com/in/en", timeout=60000)
            print("Step 1: navigated to Puma site - success")

            # Step 2: click Allow Cookies (xpath provided earlier)
            cookie_xpath = "xpath=//*[@id='puma-skip-here']/div[2]/div/div/div/button[2]"
            click_when_visible(page, cookie_xpath, "Step 2: click Allow Cookies")

            # Step 3: open search panel and wait for input
            if not open_search_and_wait(page, timeout_seconds=25):
                print("Step 3: could not open search panel, stopping")
                browser.close()
                return

            # Step 4: focus provided search input xpath and type query
            # user provided search bar xpath: //*[@id="983"]
            search_input_xpath = "xpath=//*[@id='983']"
            try:
                page.wait_for_selector(search_input_xpath, timeout=5000)
                search_input = page.locator(search_input_xpath).first
                # click to focus and fill
                search_input.click()
                search_input.fill("Girls Shoe")
                page.keyboard.press("Enter")
                print("Step 4: searched for 'Girls Shoe' using provided search input - success")
            except Exception:
                # fallback: use generic search input
                fallback_selector = "input[placeholder*='Search'], input[type='search'], input[id*='search']"
                try:
                    page.wait_for_selector(fallback_selector, timeout=5000)
                    fallback_input = page.locator(fallback_selector).first
                    fallback_input.click()
                    fallback_input.fill("Girls Shoe")
                    page.keyboard.press("Enter")
                    print("Step 4: searched for 'Girls Shoe' using fallback input - success")
                except Exception as e:
                    print("Step 4: could not perform search - failed:", str(e))
                    save_debug(page, "search_input_fail")
                    browser.close()
                    return

            # Step 5: wait for product list to appear
            product_list_selector = "xpath=//*[@id='product-list-items']"
            try:
                page.wait_for_selector(product_list_selector, timeout=10000)
                print("Step 5: product list visible - success")
            except Exception:
                print("Step 5: product list not found within timeout; proceeding anyway")

            # Step 6: click Girls checkbox if available (user-provided xpath)
            girls_checkbox_xpath = "xpath=//*[@id='puma-skip-here']/div/section/nav[1]/div/div/div/div[1]/div[2]/ul/li[4]/div/div/div/div[2]/div/ul/li[5]/label/div[1]"
            click_when_visible(page, girls_checkbox_xpath, "Step 6: click Girls checkbox (if present)")

            # Step 7: click first product (user-provided xpath)
            first_product_xpath = "xpath=//*[@id='product-list-items']/li[1]"
            try:
                page.wait_for_selector(first_product_xpath, timeout=10000)
                # click the element; prefer clicking the anchor if exists
                try:
                    page.locator(first_product_xpath + "/ancestor::a[1]").first.click()
                except Exception:
                    page.locator(first_product_xpath).first.click()
                print("Step 7: clicked first product - success")
            except Exception as e:
                print("Step 7: could not click first product - failed:", str(e))
                save_debug(page, "first_product_fail")
                browser.close()
                return

            # Step 8: wait for product detail page
            page.wait_for_load_state("networkidle", timeout=20000)
            print("Step 8: product detail page loaded - success")

            # Step 9: select size 14-Y (best-effort)
            size_variants = ["14-Y", "14 Y", "14Y", "14 Youth", "14 - Y", "14"]
            size_selected = False
            for sv in size_variants:
                sel = f"button:has-text('{sv}'), span:has-text('{sv}'), li:has-text('{sv}')"
                try:
                    if page.locator(sel).count() > 0:
                        page.locator(sel).filter(lambda el: el.is_visible()).first.click()
                        print("Step 9: selected size", sv, "- success")
                        size_selected = True
                        break
                except Exception:
                    continue
            if not size_selected:
                print("Step 9: size 14-Y not found automatically; continuing")

            # Step 10: click Add to Cart (best-effort)
            add_selectors = [
                "button:has-text('Add to cart')",
                "button:has-text('Add to Bag')",
                "button:has-text('ADD TO BAG')",
                "button[data-testid*='add-to-cart']",
                "button[class*='add-to-cart']"
            ]
            added = False
            for sel in add_selectors:
                try:
                    if page.locator(sel).count() > 0:
                        page.locator(sel).first.click()
                        print("Step 10: clicked Add to Cart - success (selector: " + sel + ")")
                        added = True
                        break
                except Exception:
                    continue
            if not added:
                print("Step 10: Add to Cart not found or failed")

            # Final: save snapshot and finish
            save_debug(page, "final_state")
            print("Flow completed. Check browser and debug files if any step failed.")

        except Exception as e:
            print("Unhandled exception:", str(e))
            try:
                save_debug(page, "unhandled_exception")
            except Exception:
                pass
        finally:
            browser.close()

if __name__ == "__main__":
    run()

