from st_pages import Page, Section, show_pages, add_page_title

show_pages(
    [   Page(r"C:/Users/khanh/Documents/Market Analyst/Home.py", "Home", "🏠"),
        Page(r"C:/Users/khanh/Documents/Market Analyst/Sales_performance.py", "Top Sales Corporation", "📊"),
        Section(name="Benchmark company performance vs. market", icon="📈"),
          Page(r"C:/Users/khanh/Documents/Market Analyst/Overview.py", "Overview"),
          Page(r"C:/Users/khanh/Documents/Market Analyst/Mocules.py", "Mocules"),
          Page(r"C:/Users/khanh/Documents/Market Analyst/Content.py", "Content"),
          Page(r"C:/Users/khanh/Documents/Market Analyst/Channel.py", "Channel"),
          Page(r"C:/Users/khanh/Documents/Market Analyst/Branded_GX.py", "Branded_GX"),

    ]
)

add_page_title()
