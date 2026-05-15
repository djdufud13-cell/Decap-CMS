#!/usr/bin/env python3
import re
import html

def generate_slug(title, article_num):
    """Generate URL slug from title"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    slug = slug[:60]
    return f"{article_num}-{slug}"

def markdown_to_html(text):
    """Convert markdown to HTML"""
    # Headers
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Lists
    text = re.sub(r'^- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    
    # Paragraphs (wrap non-tag lines in <p>)
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            result.append('')
        elif line.startswith('<h') or line.startswith('<li') or line.startswith('</'):
            result.append(line)
        else:
            result.append(f'<p>{line}</p>')
    
    return '\n'.join(result)

def create_article_html(article_num, title, body, keywords, date_str="2026-05-15"):
    slug = generate_slug(title, article_num)
    filename = f"{slug}.html"
    
    # Extract excerpt from body
    excerpt = body.split('\n\n')[1][:200] if '\n\n' in body else body[:200]
    excerpt = re.sub(r'[#*]', '', excerpt).strip()
    
    # Convert markdown to HTML
    body_html = markdown_to_html(body)
    
    # Extract category from keywords
    if 'manufacturer' in keywords.lower():
        category = "Market Analysis"
    elif 'supplier' in keywords.lower():
        category = "Supplier Selection"
    else:
        category = "Procurement"
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Liu's Blog</title>
  <meta name="description" content="{excerpt}...">
  <link rel="canonical" href="https://liudeboke.com/posts/en/{filename}">
  <link rel="alternate" hreflang="zh" href="https://liudeboke.com/posts/zh/{filename}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/style.css">

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-W5BZLQWDZK"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-W5BZLQWDZK');
  </script>
  <meta name="google-site-verification" content="aaKmOZPoxWUIpNsa7FQNVaO5Dpxc0y3ZQKDablh9StA">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@hualingmachinery">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{excerpt}...">
  <meta name="twitter:image" content="https://liudeboke.com/assets/images/og-article.png">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{excerpt}...">
  <meta property="og:url" content="https://liudeboke.com/posts/en/{filename}">
  <meta property="og:image" content="https://liudeboke.com/assets/images/og-article.png">
  <meta property="og:site_name" content="Liu's Blog">
  <meta property="article:published_time" content="{date_str}T08:00:00+08:00">
</head>
<body>

  <nav class="navbar">
    <div class="container">
      <div class="navbar-inner">
        <a href="https://liudeboke.com/index_en.html" class="navbar-brand">
          <div class="navbar-logo">L</div>
          <span>Liu's Blog</span>
        </a>
        <div class="navbar-nav" role="menubar">
          <a href="https://liudeboke.com/index_en.html">Home</a>
          <a href="../../index_en.html#about">About Liu</a>
          <a href="../../index_en.html#products">Products</a>
          <a href="index.html" style="color:var(--brand);font-weight:700;">Blog</a>
          <a href="../../index_en.html#contact">Contact</a>
        </div>
      </div>
    </div>
  </nav>

  <main class="container" style="padding:2rem 1rem;">
    <article class="article-card" style="max-width:800px;margin:0 auto;">
      <div class="article-meta">
        <span>📅 {date_str}</span>
        <span>⏱️ {category}</span>
      </div>

{body_html}

    </article>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <a href="https://liudeboke.com/index_en.html">
            <div class="footer-logo">L</div>
            <span>Liu's Blog</span>
          </a>
        </div>
        <div class="footer-links">
          <a href="mailto:info@hualingmachinery.com">Email</a>
          <a href="https://github.com/djdufud13-cell" target="_blank">GitHub</a>
        </div>
        <div class="footer-copyright">
          <p>&copy; 2026 Liu's Blog. All rights reserved.</p>
        </div>
      </div>
    </div>
  </footer>

</body>
</html>'''
    
    return filename, html_content

# Article 21
article21_title = "Phenolic Resin Mechanical Parts: Why Industrial Manufacturers Choose Bakelite in 2026"
article21_body = """# Phenolic Resin Mechanical Parts: Why Industrial Manufacturers Choose Bakelite in 2026

## Phenolic Resin Mechanical Parts Manufacturer: Introduction

In the landscape of industrial material selection, phenolic resin mechanical parts—commonly known as bakelite parts—have maintained their irreplaceable position in critical engineering applications despite the emergence of newer polymer alternatives. As global manufacturing continues to evolve in 2026, driven by volatile raw material markets, supply chain disruptions, and heightened performance demands, phenolic resin mechanical parts manufacturers are experiencing renewed strategic interest from industrial buyers across automotive, electrical, aerospace, and heavy machinery sectors.

This article examines the current market dynamics driving phenolic resin adoption, presents the latest pricing trends for key feedstocks including phenol and formaldehyde, and offers actionable procurement recommendations for businesses seeking reliable phenolic resin mechanical parts suppliers.

## Phenolic Resin Mechanical Parts Manufacturer: Understanding Phenolic Resin Mechanical Parts

Phenolic resin, chemically classified as phenol-formaldehyde resin (PF resin, CAS 9003-35-4), is one of the oldest synthetic polymers in industrial use. First commercialized in the early 20th century, phenolic resin remains indispensable due to its exceptional combination of thermal stability, mechanical strength, chemical resistance, and electrical insulating properties.

Bakelite mechanical parts are manufactured through compression molding, transfer molding, or injection molding of phenolic resin compounds mixed with reinforcing fillers such as wood flour, cotton fiber, glass fiber, or mineral reinforcements. The resulting components exhibit outstanding dimensional stability under thermal stress, low moisture absorption, and excellent resistance to weak acids, weak alkalis, and most organic solvents.

Typical applications include electrical insulators, bushings, bearings, gears, pump impellers, brake components, and structural elements in high-temperature environments where metal alternatives would fail or add unacceptable weight.

## Phenolic Resin Mechanical Parts Manufacturer: Current Market Price Dynamics in 2026

### Phenol Market Overview

Phenol, the primary feedstock for phenolic resin production, has experienced dramatic price volatility in 2026 driven by geopolitical tensions in the Middle East. According to data from 100ppi.com (Shengyishe), phenol prices in early April 2026 surged to 9,600–10,300 CNY/ton on fears of disrupted global petrochemical supply chains following the closure of the Strait of Hormuz.

Following a sharp correction on April 8, 2026—triggered by easing geopolitical tensions—prices declined approximately 2.24% in a single session. By late April and early May 2026, phenol prices stabilized in the range of 6,800–9,500 CNY/ton across major Chinese markets, with Shandong Province reporting transactions at 6,800–8,000 CNY/ton and premium grades from Yanshan Petrochemical commanding 8,000 CNY/ton.

### Formaldehyde Market Overview

Formaldehyde (37% solution), the secondary feedstock, has remained relatively stable at 1,000–1,150 CNY/ton throughout April–May 2026. Shandong Province suppliers, including Jin Sheng Run Chemical and Han Yue Chemical, quoted prices in the 1,100–1,150 CNY/ton range, while competitive offerings from smaller producers ranged from 1,000–1,050 CNY/ton. The formaldehyde market shows limited volatility compared to phenol, providing a relatively stable cost base for phenolic resin producers.

### Broader Commodity Context

The World Bank's April 2026 Commodity Markets Outlook projects global commodity prices to rise approximately 16% in 2026 compared to 2025, with energy prices increasing by up to 24%. Brent crude oil reached $118/barrel in late March 2026—its highest level since 2022—before retreating but remaining significantly elevated above 2025 averages. Goldman Sachs reported that base chemical prices surged more than 60% in recent weeks, with approximately 20% of global chemical supply disrupted.

These macro forces are directly transmitted to the phenolic resin supply chain. Phenol production is naphtha-based, meaning crude oil price movements correlate closely with phenol manufacturing costs. As of early May 2026, the upstream naphtha crack spread remains wide, supporting continued pressure on phenol prices.

## Phenolic Resin Mechanical Parts Manufacturer: Phenolic Resin Price Trends for Mechanical Parts

Based on current feedstock economics and market conditions, phenolic resin mechanical parts pricing in 2026 reflects the following dynamics:

- **Phenol cost (6,800–9,500 CNY/ton)**: High sensitivity; represents 50–60% of PF resin cost
- **Formaldehyde cost (1,000–1,150 CNY/ton)**: Moderate sensitivity; ~15–20% of PF resin cost
- **Energy costs (+24% YoY)**: Moderate upward pressure on processing costs
- **Logistics disruptions**: Variable; adds 5–15% to landed costs for imported resin
- **Demand surge (automotive, aerospace)**: Supports price firming through Q3 2026

Industry observers expect phenolic resin prices to remain elevated through Q3 2026, with a potential softening in Q4 2026 if Middle Eastern supply normalizes and crude oil prices retreat toward the World Bank's baseline forecast of $86/barrel.

## Phenolic Resin Mechanical Parts Manufacturer: Key Advantages of Phenolic Resin Mechanical Parts

**1. Superior Thermal Performance**
Phenolic resin maintains structural integrity at temperatures exceeding 200°C, making it ideal for applications in engine compartments, electrical switching gear, and industrial furnace components. Unlike thermoplastic alternatives, phenolic resin parts do not soften or deform under sustained thermal load.

**2. Excellent Electrical Insulation**
With a dielectric strength of 15–20 kV/mm and a dissipation factor that remains stable across a wide frequency range, phenolic resin is the material of choice for electrical insulation components including terminal blocks, circuit breaker housings, and high-voltage insulators.

**3. Dimensional Stability and Creep Resistance**
Under sustained mechanical load at elevated temperatures, phenolic resin exhibits minimal creep deformation—a critical requirement for precision mechanical components in automotive and aerospace applications.

**4. Chemical Resistance**
Phenolic resin mechanical parts demonstrate excellent resistance to weak acids, weak alkalis, and hydrocarbon solvents, making them suitable for chemical processing equipment, pump components, and valve seats.

**5. Friction and Wear Properties**
When compounded with appropriate fillers, phenolic resin offers low friction coefficients and excellent wear resistance, making it ideal for brake pads, clutch facings, and bearing applications.

## Phenolic Resin Mechanical Parts Manufacturer: Procurement Recommendations for 2026

For buyers seeking reliable phenolic resin mechanical parts manufacturers or custom bakelite parts manufacturers, consider the following strategic guidance:

**1. Diversify Your Supplier Base**
The current chemical supply disruption (20% global capacity affected) makes single-source procurement risky. Establish relationships with at least two to three phenolic resin mechanical parts suppliers across different geographic regions to mitigate supply disruption risk.

**2. Lock in Pricing for H2 2026 Now**
Given upward commodity price pressure and expected continued demand strength through Q3 2026, buyers should consider forward contracts for phenolic resin materials rather than relying on spot pricing. Long-term agreements of 6–12 months can provide cost predictability amid volatile feedstock markets.

**3. Monitor Phenol Price Indices Closely**
Since phenol represents the dominant cost input, tracking phenol prices on 100ppi.com and chemicalbook.com can provide advance signals for phenolic resin price movements. Price increases typically lag phenol movements by 4–6 weeks due to processing and inventory cycles.

**4. Specify Resin Grade Carefully**
Not all phenolic resins are equivalent for mechanical applications. Work with your phenolic resin mechanical parts manufacturer to specify appropriate resin grades, filler systems, and molding processes for your specific performance requirements. Custom bakelite parts manufacturer relationships often provide technical consultation as part of the sourcing process.

**5. Consider Regional Sourcing**
Chinese domestic phenolic resin producers have maintained relatively stable output in 2026 despite global disruptions. For buyers in Asia-Pacific, sourcing from established Chinese phenolic resin mechanical parts manufacturers can offer both cost and supply security advantages.

## Phenolic Resin Mechanical Parts Manufacturer: Conclusion

Phenolic resin mechanical parts continue to demonstrate compelling value propositions in 2026, with market fundamentals—driven by tight feedstock supplies, elevated crude oil prices, and robust demand from key end-use sectors—supporting a firm pricing environment through at least mid-year.

Buyers who establish strategic relationships with experienced phenolic resin mechanical parts manufacturers now will be best positioned to secure supply, manage costs, and access the technical expertise necessary to optimize part design for their specific applications. The combination of phenolic resin's proven performance characteristics and the strategic importance of resilient supply chains makes proactive supplier engagement a high-priority initiative for engineering procurement teams in 2026."""

article21_keywords = "phenolic resin mechanical parts manufacturer, bakelite mechanical parts manufacturer, phenolic resin parts price 2026"

# Article 22
article22_title = "Phenolic Resin Mechanical Parts Supplier: Global Sourcing Strategies and Market Outlook 2026"
article22_body = """# Phenolic Resin Mechanical Parts Supplier: Global Sourcing Strategies and Market Outlook 2026

## Phenolic Resin Mechanical Parts Supplier: Introduction

The global phenolic resin mechanical parts supplier market enters mid-2026 at a critical inflection point. Elevated feedstock costs, persistent supply chain disruptions affecting approximately 20% of global chemical capacity, and intensifying demand from automotive, electrical, and industrial machinery sectors have reshaped the competitive landscape for phenolic resin mechanical parts suppliers worldwide.

For procurement professionals and supply chain managers tasked with sourcing phenolic resin mechanical parts, understanding the current market dynamics, regional supplier capabilities, and emerging industry trends is essential for optimizing sourcing strategies and ensuring reliable supply.

This article provides a comprehensive market overview, profiles key supplier regions and capabilities, presents the latest phenol and formaldehyde pricing intelligence, and delivers actionable sourcing recommendations for buyers navigating the 2026 phenolic resin mechanical parts procurement landscape.

## Phenolic Resin Mechanical Parts Supplier: Global Market Overview in 2026

### Macro Drivers Affecting Supplier Markets

The World Bank's April 2026 Commodity Markets Outlook provides the essential macroeconomic backdrop for phenolic resin mechanical parts procurement:

- **Global commodity prices**: Projected to rise approximately 16% year-over-year in 2026
- **Energy prices**: Forecast to increase by up to 24% compared to 2025
- **Crude oil**: Brent crude reached $118/barrel in late March 2026 (highest since 2022) before retreating; World Bank baseline forecast of $86/barrel for full-year 2026

Goldman Sachs analysis indicates that base chemical prices have surged more than 60% in recent weeks, with the Strait of Hormuz closure creating sustained disruption to Middle Eastern petrochemical exports. This geopolitical reality directly impacts phenolic resin mechanical parts suppliers, as phenol—the primary feedstock—derives from naphtha, which tracks crude oil pricing.

### Regional Supplier Dynamics

**China (Asia-Pacific Manufacturing Hub)**

China remains the dominant global producer of phenolic resin and phenolic resin mechanical parts. Chinese phenolic resin mechanical parts suppliers benefit from:

- Integrated upstream phenol and formaldehyde supply chains
- Large-scale compression and transfer molding manufacturing infrastructure
- Competitive labor and energy costs
- Established export logistics to North America, Europe, and Southeast Asia

Despite global disruptions, Chinese domestic phenolic resin production has remained relatively stable, providing Asian-Pacific buyers with a relatively secure supply corridor.

**Europe**

European phenolic resin mechanical parts suppliers face significant headwinds from elevated energy costs. Natural gas prices rose 59% in March 2026, and electricity costs remain 30–40% above 2024 levels. This energy-intensive production environment pressures European suppliers' cost competitiveness, though proximity to automotive and aerospace OEM supply chains remains a strategic advantage.

**North America**

North American phenolic resin mechanical parts suppliers have benefited from relatively stable domestic naphtha and natural gas feedstocks compared to European competitors. U.S. phenol production has maintained healthy operating rates, though feedstock cost pass-throughs have pushed PF resin prices 20–30% above 2025 levels.

## Phenolic Resin Mechanical Parts Supplier: Phenol and Formaldehyde Price Intelligence

### Phenol Price Analysis

Based on data from 100ppi.com (Shengyishe) and chemicalbook.com, phenol pricing as of May 2026 reflects the following market structure:

- **Peak pricing (early April 2026)**: 9,600–10,300 CNY/ton triggered by Hormuz Strait tensions
- **Correction (April 8, 2026)**: Single-day decline of 2.24% following ceasefire signals
- **Current stabilization (late April–early May 2026)**: 6,800–9,500 CNY/ton across major Chinese markets
- **Regional variations**: Shandong Province: 6,800–8,000 CNY/ton; Yanshan Petrochemical premium grade: 8,000 CNY/ton

Phenol pricing exhibits high beta sensitivity to crude oil movements. Given the World Bank's $86/barrel baseline crude forecast for 2026, phenol prices are expected to remain in the 6,500–9,000 CNY/ton range through Q3 2026, with upside risk if Middle Eastern supply disruptions persist.

### Formaldehyde Price Analysis

Formaldehyde (37% solution) pricing has demonstrated relative stability:

- **April–May 2026 range**: 1,000–1,150 CNY/ton
- **Shandong Province quotes**: 1,100–1,150 CNY/ton (Jin Sheng Run Chemical, Han Yue Chemical)
- **Competitive regional quotes**: 1,000–1,050 CNY/ton

The methanol-based formaldehyde production process provides a more stable cost base, with methanol pricing less directly correlated to crude oil than phenol.

### Phenolic Resin (PF Resin) Cost Implications

For a phenolic resin mechanical parts supplier, the cost structure typically breaks down as:

| Cost Component | Proportion | Current Price Range (May 2026) |
|---|---|---|
| Phenol feedstock | 50–60% | 6,800–9,500 CNY/ton |
| Formaldehyde feedstock | 15–20% | 1,000–1,150 CNY/ton |
| Energy and processing | 15–25% | Elevated (+24% YoY) |
| Fillers and additives | 5–10% | Relatively stable |
| Labor and overhead | 10–15% | Regional variation |

## Phenolic Resin Mechanical Parts Supplier: Evaluation Framework

### Technical Capability Assessment

When qualifying phenolic resin mechanical parts suppliers, evaluate the following technical dimensions:

**Material Range**: Does the supplier offer both thermosetting and thermoplastic phenolic resin grades? Can they compound custom formulations for specific thermal, electrical, or mechanical performance targets?

**Molding Capabilities**: Assess available forming processes (compression, transfer, injection, SMC/BMC), maximum part dimensions, and dimensional tolerance capabilities. Some phenolic resin mechanical parts suppliers specialize in small precision parts while others focus on large structural components.

**Testing and Certification**: Verify the supplier's testing capabilities including mechanical property testing (tensile, flexural, impact), thermal analysis (DSC, TGA), electrical testing (dielectric strength, volume resistivity), and flammability testing (UL 94). Third-party certification (ISO 9001, IATF 16949, AS9100D) provides independent quality assurance.

### Production Capacity Evaluation

Understanding a phenolic resin mechanical parts supplier's production capacity and utilization is critical for supply security:

- **Monthly phenolic resin compound throughput**: 100–500+ metric tons for mid-scale suppliers
- **Molding machine count and capacity**: Fleet size and age distribution
- **Lead time capabilities**: Standard lead times of 3–6 weeks for production orders; prototype tooling 2–4 weeks
- **Capacity reservation options**: Can the supplier dedicate capacity for your annual volume requirements?

### Financial Stability Assessment

A phenolic resin mechanical parts supplier's financial health directly impacts supply continuity. Evaluate:

- **Credit terms offered**: Net 30/60/90 days; letter of credit arrangements
- **Working capital adequacy**: Ability to carry raw material inventory for multi-month supply contracts
- **Industry tenure and reputation**: Established track record in phenolic resin mechanical parts manufacturing
- **Customer references**: Obtain references from buyers in your industry segment

## Phenolic Resin Mechanical Parts Supplier: Emerging Trends Shaping Supplier Relationships in 2026

### 1. Vertical Integration Accelerating

Leading phenolic resin mechanical parts suppliers are increasingly pursuing vertical integration, securing phenol supply through strategic partnerships or joint ventures with upstream chemical producers. This integration provides cost visibility and supply security advantages that mid-scale and smaller suppliers cannot match.

### 2. Sustainability Requirements Emerging

Environmental regulations and OEM sustainability mandates are beginning to influence phenolic resin mechanical parts procurement:

- EU REACH compliance requirements for phenol and formaldehyde
- Low-formaldehyde emission grades for interior applications
- Recycling and end-of-life considerations for phenolic resin waste
- Carbon footprint disclosure requirements from major automotive OEMs

Suppliers who proactively address sustainability requirements will gain competitive advantage in the automotive and consumer goods supply chains.

### 3. Digital Procurement Integration

Leading phenolic resin mechanical parts suppliers are investing in digital procurement interfaces—supplier portals, electronic data interchange (EDI), and API-based order management—enabling buyers to streamline purchase order management, track shipment status in real-time, and access technical documentation digitally.

## Phenolic Resin Mechanical Parts Supplier: Strategic Sourcing Recommendations

### For North American and European Buyers

**Diversify across Asia-Pacific and domestic suppliers**: Leverage Chinese phenolic resin mechanical parts suppliers for cost competitiveness and supply volume, while maintaining domestic or near-shore suppliers for JIT delivery and engineering collaboration requirements.

**Structure indexed pricing contracts**: Tie raw material cost pass-throughs to published phenol price indices (100ppi.com phenol index) rather than fixed pricing, reducing supplier risk premium and improving cost transparency.

### For Asia-Pacific Buyers

**Leverage domestic supply advantages**: Chinese and Southeast Asian buyers benefit from shorter supply chains and established phenolic resin mechanical parts supplier ecosystems. Focus qualification efforts on domestic suppliers with proven track records in your specific industry segment.

**Negotiate volume commitments with price tiers**: Consolidated annual volume commitments of 100+ metric tons of phenolic resin compound equivalent can unlock meaningful pricing benefits from established suppliers.

### For All Buyers

**Qualify backup suppliers now**: Given ongoing supply chain volatility, qualify at least one backup phenolic resin mechanical parts supplier for each critical part family before you need them. Qualifying a new supplier under production pressure is costly and risky.

**Engage suppliers on technical development**: Share your application roadmap with key phenolic resin mechanical parts suppliers. Proactive collaboration on next-generation part designs can yield significant material and manufacturing cost reductions.

## Phenolic Resin Mechanical Parts Supplier: Conclusion

The 2026 phenolic resin mechanical parts supplier landscape rewards buyers who combine strategic supplier relationship management with disciplined market intelligence monitoring. The current environment—characterized by elevated feedstock costs, geopolitical supply disruptions, and strong end-use demand—demands that procurement professionals maintain active engagement with their supplier base while continuously assessing market developments.

By implementing a structured supplier qualification and management framework, diversifying sourcing across regions, and structuring contracts that fairly allocate commodity price risk, buyers can secure reliable access to high-quality phenolic resin mechanical parts at predictable costs through the remainder of 2026 and into 2027."""

article22_keywords = "phenolic resin mechanical parts supplier, PF resin parts supplier, phenolic resin parts sourcing 2026"

# Generate articles
print("Generating article 21...")
filename21, html21 = create_article_html(21, article21_title, article21_body, article21_keywords)
with open(f"C:/Users/Administrator/.qclaw/workspace/liudeboke-blog/posts/en/{filename21}", "w", encoding="utf-8") as f:
    f.write(html21)
print(f"Created: {filename21}")

print("Generating article 22...")
filename22, html22 = create_article_html(22, article22_title, article22_body, article22_keywords)
with open(f"C:/Users/Administrator/.qclaw/workspace/liudeboke-blog/posts/en/{filename22}", "w", encoding="utf-8") as f:
    f.write(html22)
print(f"Created: {filename22}")

print("\nDone!")
