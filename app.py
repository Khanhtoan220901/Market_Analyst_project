from st_pages import Page, Section, show_pages, add_page_title

show_pages(
    [   Page("Home.py", "Home", "🏠"),
        Page("Sales_performance.py", "Top Sales Corporation", "📊"),
        Section(name="Benchmark company performance vs. market", icon="📈"),
          Page("Overview.py", "Overview"),
          Page("Mocules.py", "Mocules"),
          Page("Content.py", "Content"),
          Page("Channel.py", "Channel"),
          Page("Branded_GX.py", "Branded_GX"),

    ]
)

add_page_title()
