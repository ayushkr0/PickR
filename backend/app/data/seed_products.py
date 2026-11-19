"""
MVP seed data — 5 laptops, 5 headphones, 5 cameras.
Each product has a rich `searchable_text` field used to generate embeddings.
"""

PRODUCTS = [
    # ── LAPTOPS ──────────────────────────────────────────────────────────────
    {
        "name": "Apple MacBook Air 15-inch (M3)",
        "category": "laptop",
        "brand": "Apple",
        "price": 1299.00,
        "image_url": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mba15-midnight-select-202402",
        "affiliate_url": "https://www.amazon.com/dp/B0CX23V2ZK",
        "specs": {
            "chip": "Apple M3",
            "ram": "8GB",
            "storage": "256GB SSD",
            "display": "15.3-inch Liquid Retina",
            "battery_hours": 18,
            "weight_lbs": 3.3,
            "os": "macOS",
        },
        "summary": "The best thin-and-light laptop for everyday use and creative work, with all-day battery life.",
        "pros": [
            "Exceptional battery life (up to 18 hours)",
            "Silent — completely fanless design",
            "Brilliant Retina display",
            "Great for students and professionals alike",
        ],
        "cons": [
            "Base RAM (8GB) can feel limited for heavy multitasking",
            "No built-in ports beyond 2x USB-C",
            "Premium price over Windows alternatives",
        ],
        "searchable_text": (
            "MacBook Air M3 Apple lightweight thin silent fanless student creative work "
            "photo editing video editing long battery life macOS 15 inch portable college "
            "everyday use productivity good battery lightweight travel"
        ),
    },
    {
        "name": "Dell XPS 15 (9530)",
        "category": "laptop",
        "brand": "Dell",
        "price": 1499.00,
        "image_url": "/products/dell-xps-15.png",
        "affiliate_url": "https://www.amazon.com/dp/B0BZJHGBFC",
        "specs": {
            "chip": "Intel Core i7-13700H",
            "ram": "16GB DDR5",
            "storage": "512GB NVMe SSD",
            "display": "15.6-inch OLED 3.5K",
            "battery_hours": 13,
            "weight_lbs": 4.2,
            "os": "Windows 11",
            "gpu": "NVIDIA RTX 4060",
        },
        "summary": "A premium Windows powerhouse with a stunning OLED display — ideal for developers and content creators.",
        "pros": [
            "Gorgeous OLED display with deep blacks",
            "Strong performance for dev and creative tasks",
            "Solid build quality with CNC aluminum chassis",
            "Dedicated GPU handles light gaming and rendering",
        ],
        "cons": [
            "Battery life shorter than MacBook Air",
            "Runs warm under heavy load",
            "Expensive for the spec sheet",
        ],
        "searchable_text": (
            "Dell XPS 15 Windows developer programming coding OLED display beautiful screen "
            "content creator video editing photo editing RTX GPU gaming light gaming "
            "powerful performance professional work heavy tasks multitasking"
        ),
    },
    {
        "name": "Lenovo ThinkPad X1 Carbon Gen 11",
        "category": "laptop",
        "brand": "Lenovo",
        "price": 1349.00,
        "image_url": "https://p1-ofp.static.pub/medias/bWFzdGVyfHJvb3R8MzE2NzU2fGltYWdlL3BuZ3xoMjkvaGU3LzEzMTM0MTU2MDY4NjM4",
        "affiliate_url": "https://www.amazon.com/dp/B0BVFZLZJX",
        "specs": {
            "chip": "Intel Core i7-1365U",
            "ram": "16GB LPDDR5",
            "storage": "512GB SSD",
            "display": "14-inch IPS 2.8K",
            "battery_hours": 15,
            "weight_lbs": 2.48,
            "os": "Windows 11 Pro",
        },
        "summary": "The gold standard for business travel — ultra-light, military-grade durable, and supremely reliable.",
        "pros": [
            "Lightest premium 14-inch laptop at 2.48 lbs",
            "Military-grade durability (MIL-SPEC tested)",
            "Excellent keyboard — best in class",
            "Long battery life with rapid charge",
        ],
        "cons": [
            "Display not as vibrant as OLED rivals",
            "No dedicated GPU",
            "Business-oriented looks — not flashy",
        ],
        "searchable_text": (
            "ThinkPad X1 Carbon business travel lightweight ultralight durable reliable "
            "keyboard typing executive professional corporate work Windows frequent flyer "
            "portable commute MIL-SPEC rugged dependable long battery"
        ),
    },
    {
        "name": "ASUS ROG Zephyrus G14 (2024)",
        "category": "laptop",
        "brand": "ASUS",
        "price": 1599.00,
        "image_url": "https://dlcdnwebimgs.asus.com/gain/FC7DB99A-F98B-4B62-A2EB-B0B7E8B7E6D0",
        "affiliate_url": "https://www.amazon.com/dp/B0CRJ8DL9J",
        "specs": {
            "chip": "AMD Ryzen 9 8945HS",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD",
            "display": "14-inch OLED 2.8K 120Hz",
            "battery_hours": 10,
            "weight_lbs": 3.5,
            "os": "Windows 11",
            "gpu": "NVIDIA RTX 4070",
        },
        "summary": "A compact gaming beast that doubles as a creative workstation — rare power in a 14-inch frame.",
        "pros": [
            "RTX 4070 GPU handles AAA games and 3D rendering",
            "OLED display with 120Hz refresh rate",
            "32GB RAM — no multitasking limits",
            "Surprisingly compact for its power",
        ],
        "cons": [
            "Battery life drops fast during gaming",
            "Gets loud under sustained GPU load",
            "Pricier than many gaming laptops",
        ],
        "searchable_text": (
            "ASUS ROG gaming laptop high performance AAA games 3D rendering animation "
            "RTX 4070 GPU powerful compact portable gamer streaming video editing "
            "high refresh rate OLED 32GB RAM fast storage multitasking"
        ),
    },
    {
        "name": "Acer Aspire 5 (A515-58M)",
        "category": "laptop",
        "brand": "Acer",
        "price": 599.00,
        "image_url": "/products/acer-aspire-5.png",
        "affiliate_url": "https://www.amazon.com/dp/B0CJM4NZ6M",
        "specs": {
            "chip": "Intel Core i5-1335U",
            "ram": "8GB DDR5",
            "storage": "512GB SSD",
            "display": "15.6-inch IPS FHD",
            "battery_hours": 9,
            "weight_lbs": 3.97,
            "os": "Windows 11 Home",
        },
        "summary": "The best budget laptop for students and everyday tasks — solid performance without breaking the bank.",
        "pros": [
            "Very affordable at under $600",
            "Fast SSD and responsive performance",
            "Full-size HDMI and USB-A ports",
            "Lightweight enough for daily carry",
        ],
        "cons": [
            "Display brightness could be better",
            "Build feels plasticky compared to premium rivals",
            "No dedicated GPU",
        ],
        "searchable_text": (
            "Acer Aspire budget affordable cheap student first laptop everyday tasks "
            "web browsing email documents spreadsheets zoom calls school college "
            "basic use low price good value Windows beginner"
        ),
    },

    # ── HEADPHONES ───────────────────────────────────────────────────────────
    {
        "name": "Sony WH-1000XM5",
        "category": "headphone",
        "brand": "Sony",
        "price": 349.99,
        "image_url": "https://www.sony.com/image/5d02da5df552836db894cead8a68f5f3",
        "affiliate_url": "https://www.amazon.com/dp/B09XS7JWHH",
        "specs": {
            "type": "Over-ear",
            "anc": True,
            "driver_size_mm": 30,
            "battery_hours": 30,
            "multipoint": True,
            "codec": ["AAC", "SBC", "LDAC"],
            "foldable": False,
        },
        "summary": "The best overall noise-cancelling headphones — industry-leading ANC with natural sound and all-day comfort.",
        "pros": [
            "Best-in-class noise cancellation",
            "Exceptional 30-hour battery life",
            "Comfortable for long listening sessions",
            "Multipoint: connect to 2 devices at once",
        ],
        "cons": [
            "Not foldable — bulkier to travel with",
            "Call quality can struggle in very loud environments",
            "Premium price",
        ],
        "searchable_text": (
            "Sony WH-1000XM5 noise cancelling ANC commute office open plan focus work "
            "travel airplane flight comfortable all-day wear long listening premium "
            "wireless Bluetooth over-ear music quality LDAC hi-res"
        ),
    },
    {
        "name": "Apple AirPods Pro (2nd Gen)",
        "category": "headphone",
        "brand": "Apple",
        "price": 249.00,
        "image_url": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/MQD83",
        "affiliate_url": "https://www.amazon.com/dp/B0BDHWDR12",
        "specs": {
            "type": "In-ear",
            "anc": True,
            "driver_size_mm": 11,
            "battery_hours": 6,
            "battery_with_case_hours": 30,
            "multipoint": False,
            "codec": ["AAC", "SBC"],
            "water_resistance": "IPX4",
        },
        "summary": "The best earbuds for iPhone users — seamless Apple ecosystem integration with great ANC in a compact form.",
        "pros": [
            "Instant pairing and seamless Apple device switching",
            "Great ANC and Transparency mode",
            "Compact and easy to carry everywhere",
            "IPX4 water resistant — safe for workouts",
        ],
        "cons": [
            "Short 6-hour bud battery (30 with case)",
            "Best only within Apple ecosystem",
            "No LDAC/aptX for hi-res audio",
        ],
        "searchable_text": (
            "AirPods Pro Apple iPhone ecosystem seamless switching compact gym workout "
            "running fitness water resistant commute portable small earbuds in-ear ANC "
            "calls meetings transparency mode everyday use"
        ),
    },
    {
        "name": "Bose QuietComfort 45",
        "category": "headphone",
        "brand": "Bose",
        "price": 279.00,
        "image_url": "https://assets.bose.com/content/dam/Bose_DAM/Web/consumer_electronics/global/products/headphones/qc45",
        "affiliate_url": "https://www.amazon.com/dp/B098FKXT8L",
        "specs": {
            "type": "Over-ear",
            "anc": True,
            "driver_size_mm": 40,
            "battery_hours": 24,
            "multipoint": True,
            "codec": ["AAC", "SBC"],
            "foldable": True,
        },
        "summary": "Legendary comfort with excellent ANC — the go-to for frequent flyers and long work sessions.",
        "pros": [
            "Supremely comfortable — wear for hours",
            "Great ANC, especially for low-frequency noise",
            "Foldable and travel-friendly",
            "Simple, no-fuss controls",
        ],
        "cons": [
            "Sound signature is bass-light vs rivals",
            "No LDAC or aptX",
            "App is basic compared to Sony",
        ],
        "searchable_text": (
            "Bose QC45 comfort long wear travel flight airplane frequent flyer work from home "
            "focus office noise cancelling foldable portable simple easy to use "
            "over-ear wireless Bluetooth all-day comfortable"
        ),
    },
    {
        "name": "Sennheiser HD 560S",
        "category": "headphone",
        "brand": "Sennheiser",
        "price": 149.00,
        "image_url": "https://assets.sennheiser.com/img/15305/x1_desktop_HD-560S-Sennheiser-headphones.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B08G4PXKBD",
        "specs": {
            "type": "Over-ear",
            "anc": False,
            "driver_size_mm": 38,
            "open_back": True,
            "wired": True,
            "impedance_ohms": 120,
            "frequency_response": "6Hz–38kHz",
        },
        "summary": "Audiophile-grade wired headphones at an accessible price — best for critical listening at home.",
        "pros": [
            "Wide, natural soundstage from open-back design",
            "Accurate, reference-level sound for audiophiles",
            "Lightweight and comfortable",
            "Great value for sound quality delivered",
        ],
        "cons": [
            "Open-back leaks sound — not for public use",
            "Wired only — no Bluetooth",
            "No noise cancellation",
        ],
        "searchable_text": (
            "Sennheiser HD 560S audiophile wired open-back home listening music enthusiast "
            "critical listening reference sound studio accurate natural soundstage "
            "budget hi-fi affordable high fidelity music lover at home"
        ),
    },
    {
        "name": "Jabra Evolve2 55",
        "category": "headphone",
        "brand": "Jabra",
        "price": 449.00,
        "image_url": "https://www.jabra.com/globalassets/products/professional/jabra-evolve/evolve2-55/gallery/evolve2-55-gallery-main.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B09248BVHZ",
        "specs": {
            "type": "Over-ear",
            "anc": True,
            "driver_size_mm": 40,
            "battery_hours": 36,
            "multipoint": True,
            "microphones": 10,
            "uc_certified": True,
        },
        "summary": "The best headset for remote professionals — crystal-clear calls and elite noise cancellation built for meetings.",
        "pros": [
            "10-mic array gives outstanding call clarity",
            "36-hour battery — charge once, use all week",
            "UC certified (Zoom, Teams, Google Meet)",
            "Comfortable for all-day wear",
        ],
        "cons": [
            "Expensive — priced for business budgets",
            "Bulky design not ideal for commuting",
            "Overkill for casual music listening",
        ],
        "searchable_text": (
            "Jabra Evolve2 business professional remote work meetings calls Zoom Teams "
            "Microsoft conference call clarity microphone home office work from home "
            "all day comfort long battery UC certified enterprise"
        ),
    },

    # ── CAMERAS ──────────────────────────────────────────────────────────────
    {
        "name": "Sony ZV-E10 II",
        "category": "camera",
        "brand": "Sony",
        "price": 799.00,
        "image_url": "https://www.sony.com/image/ZVE10M2_body",
        "affiliate_url": "https://www.amazon.com/dp/B0D5C2S4PG",
        "specs": {
            "sensor": "APS-C 26MP",
            "sensor_size": "APS-C",
            "megapixels": 26,
            "video": "4K 60fps",
            "autofocus": "AI subject recognition",
            "stabilization": "Electronic",
            "mount": "Sony E-mount",
            "battery_shots": 490,
        },
        "summary": "The best beginner mirrorless camera for vloggers and content creators — smart AF and excellent video.",
        "pros": [
            "AI autofocus tracks faces, eyes, and subjects perfectly",
            "4K 60fps video — great for YouTube and social",
            "Compact and lightweight body",
            "Huge Sony E-mount lens ecosystem",
        ],
        "cons": [
            "No in-body optical stabilization",
            "Screen doesn't fully articulate",
            "Kit lens is just okay",
        ],
        "searchable_text": (
            "Sony ZV-E10 II vlog YouTube content creator beginner mirrorless camera "
            "video 4K autofocus face tracking compact lightweight social media "
            "Instagram TikTok streaming affordable first camera interchangeable lens"
        ),
    },
    {
        "name": "Canon EOS R50",
        "category": "camera",
        "brand": "Canon",
        "price": 679.00,
        "image_url": "https://www.usa.canon.com/shop/p/eos-r50",
        "affiliate_url": "https://www.amazon.com/dp/B0BSDM67KQ",
        "specs": {
            "sensor": "APS-C 24.2MP",
            "sensor_size": "APS-C",
            "megapixels": 24,
            "video": "4K 30fps",
            "autofocus": "Dual Pixel CMOS AF II",
            "stabilization": "Electronic",
            "mount": "Canon RF-S mount",
            "battery_shots": 300,
        },
        "summary": "The friendliest beginner mirrorless camera — Canon's legendary colors and foolproof autofocus.",
        "pros": [
            "Best-in-class beginner autofocus (Dual Pixel)",
            "Beautiful Canon color science out of camera",
            "Lightweight and very easy to use",
            "Fully articulating touchscreen",
        ],
        "cons": [
            "Smaller RF-S lens ecosystem vs Sony E",
            "Battery life is below average",
            "4K is cropped at 30fps",
        ],
        "searchable_text": (
            "Canon EOS R50 beginner easy to use mirrorless first camera family travel "
            "photography portraits photos color accurate autofocus reliable "
            "everyday photography holiday vacation lightweight flip screen vlog"
        ),
    },
    {
        "name": "Fujifilm X100VI",
        "category": "camera",
        "brand": "Fujifilm",
        "price": 1599.00,
        "image_url": "https://fujifilm-x.com/global/products/cameras/x100vi/img/overview/main.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B0CRPKGGY6",
        "specs": {
            "sensor": "APS-C 40MP X-Trans CMOS 5 HR",
            "sensor_size": "APS-C",
            "megapixels": 40,
            "video": "6.2K 30fps",
            "autofocus": "Phase detection AI",
            "stabilization": "In-body 5-axis IBIS",
            "lens": "Fixed 23mm f/2 (35mm equiv)",
            "battery_shots": 450,
        },
        "summary": "The most stylish and capable compact camera — a fixed-lens street and travel icon with film simulation magic.",
        "pros": [
            "40MP sensor — incredible detail and crop flexibility",
            "In-body stabilization on a compact",
            "Gorgeous film simulations (Velvia, Classic Chrome)",
            "Retro design that draws less attention",
        ],
        "cons": [
            "Fixed lens — no zoom or swappable glass",
            "High demand means hard to find in stock",
            "Steep price for a fixed-lens camera",
        ],
        "searchable_text": (
            "Fujifilm X100VI street photography travel compact fixed lens retro style "
            "film simulation aesthetic cinematic look 40MP high resolution "
            "portable discreet documentary journalism walk-around everyday carry"
        ),
    },
    {
        "name": "Nikon Z5 II",
        "category": "camera",
        "brand": "Nikon",
        "price": 1699.00,
        "image_url": "https://imaging.nikon.com/lineup/mirrorless/z_5ii/img/top/top_img01.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B0CX8FW3B6",
        "specs": {
            "sensor": "Full-frame 24.5MP BSI CMOS",
            "sensor_size": "Full-frame",
            "megapixels": 24,
            "video": "4K 30fps uncropped",
            "autofocus": "Phase detect with subject recognition",
            "stabilization": "In-body 5-axis IBIS",
            "mount": "Nikon Z mount",
            "battery_shots": 740,
        },
        "summary": "The best value full-frame camera for photographers stepping up from APS-C — exceptional low-light and IBIS.",
        "pros": [
            "Full-frame sensor — superior low-light and bokeh",
            "740-shot battery life — exceptional",
            "In-body stabilization for handheld shooting",
            "Dual card slots for professional workflow",
        ],
        "cons": [
            "Heavier than APS-C cameras",
            "4K video is more limited vs Sony rivals",
            "Z-mount lenses can be expensive",
        ],
        "searchable_text": (
            "Nikon Z5 II full-frame step up upgrade serious photographer portrait "
            "low light wedding event landscape nature photography IBIS stabilization "
            "blurry background bokeh professional quality large sensor"
        ),
    },
    {
        "name": "GoPro HERO13 Black",
        "category": "camera",
        "brand": "GoPro",
        "price": 399.00,
        "image_url": "https://community.gopro.com/html/assets/HERO13Black.png",
        "affiliate_url": "https://www.amazon.com/dp/B0CFC8V9BH",
        "specs": {
            "sensor": "1/1.9-inch 27MP",
            "sensor_size": "1/1.9-inch",
            "megapixels": 27,
            "video": "5.3K 60fps",
            "stabilization": "HyperSmooth 6.0",
            "waterproof_meters": 10,
            "mount": "GoPro Ecosystem",
            "battery_hours": 2.5,
        },
        "summary": "The ultimate action camera — waterproof, ultra-stabilized, and built for adventure sports and outdoor activities.",
        "pros": [
            "Waterproof to 10m — no housing needed",
            "HyperSmooth stabilization eliminates shake",
            "Tiny and mountable anywhere (helmet, bike, chest)",
            "5.3K video with great dynamic range",
        ],
        "cons": [
            "Short ~2.5hr battery life",
            "Not ideal for low-light photography",
            "Limited manual control vs mirrorless",
        ],
        "searchable_text": (
            "GoPro HERO13 action camera adventure sports outdoor hiking surfing skiing "
            "snowboarding cycling bike helmet mount waterproof rugged travel adventure "
            "extreme sports POV first person vlog outdoor activities compact"
        ),
    },

    # ── MORE LAPTOPS ──────────────────────────────────────────────────────────
    {
        "name": "HP Pavilion 15 (2024)",
        "category": "laptop",
        "brand": "HP",
        "price": 549.00,
        "image_url": "/products/hp-pavilion-15.png",
        "affiliate_url": "https://www.amazon.com/dp/B0D1XH7V2N",
        "specs": {
            "chip": "AMD Ryzen 5 7530U",
            "ram": "8GB DDR4",
            "storage": "256GB SSD",
            "display": "15.6-inch IPS FHD",
            "battery_hours": 8,
            "weight_lbs": 3.75,
            "os": "Windows 11 Home",
        },
        "summary": "A reliable budget laptop for students who need a solid everyday machine without overspending.",
        "pros": [
            "Very affordable under $550",
            "Good enough performance for school work",
            "Decent build quality for the price",
        ],
        "cons": [
            "Only 256GB storage fills up fast",
            "No dedicated GPU",
            "Average display quality",
        ],
        "searchable_text": (
            "HP Pavilion budget cheap affordable student school college basic everyday "
            "web browsing documents spreadsheets email Zoom calls reliable value "
            "Windows beginner first laptop low price entry level"
        ),
    },
    {
        "name": "Lenovo IdeaPad Slim 5 (16-inch)",
        "category": "laptop",
        "brand": "Lenovo",
        "price": 749.00,
        "image_url": "/products/lenovo-ideapad-slim5.png",
        "affiliate_url": "https://www.amazon.com/dp/B0CZ5MZ4F7",
        "specs": {
            "chip": "AMD Ryzen 7 7730U",
            "ram": "16GB DDR5",
            "storage": "512GB SSD",
            "display": "16-inch IPS 2.5K",
            "battery_hours": 12,
            "weight_lbs": 3.9,
            "os": "Windows 11 Home",
        },
        "summary": "A mid-range sweet spot — 16GB RAM and a sharp 2.5K display at a fair price.",
        "pros": [
            "16GB RAM handles multitasking well",
            "Sharp 2.5K display for the price",
            "Good 12-hour battery life",
        ],
        "cons": [
            "No dedicated GPU for gaming",
            "Plastic build feels less premium",
            "Speakers are mediocre",
        ],
        "searchable_text": (
            "Lenovo IdeaPad mid-range student university college coding programming "
            "multitasking 16GB RAM sharp display productivity office work "
            "balanced value good screen everyday reliable"
        ),
    },
    {
        "name": "Apple MacBook Pro 14-inch (M4)",
        "category": "laptop",
        "brand": "Apple",
        "price": 1999.00,
        "image_url": "https://store.storeimages.cdn-apple.com/4668/as-images.apple.com/is/mbp14-m4pro-spaceblack-select-202410",
        "affiliate_url": "https://www.amazon.com/dp/B0DL5SLQZB",
        "specs": {
            "chip": "Apple M4 Pro",
            "ram": "24GB Unified",
            "storage": "512GB SSD",
            "display": "14.2-inch Liquid Retina XDR",
            "battery_hours": 22,
            "weight_lbs": 3.4,
            "os": "macOS",
        },
        "summary": "The ultimate creative professional laptop — M4 Pro delivers serious power in a portable package.",
        "pros": [
            "M4 Pro chip handles any creative workload",
            "22-hour battery life is unmatched",
            "XDR display with ProMotion 120Hz",
            "24GB unified memory — no bottleneck",
        ],
        "cons": [
            "High price tag",
            "Overkill for basic tasks",
            "Limited to macOS ecosystem",
        ],
        "searchable_text": (
            "MacBook Pro M4 professional creative video editing 4K 8K export "
            "3D rendering animation design photography developer coding "
            "power user pro high performance Apple macOS premium"
        ),
    },
    {
        "name": "MSI Katana 15 (2024)",
        "category": "laptop",
        "brand": "MSI",
        "price": 899.00,
        "image_url": "/products/msi-katana-15.png",
        "affiliate_url": "https://www.amazon.com/dp/B0CXK6D6F7",
        "specs": {
            "chip": "Intel Core i7-13620H",
            "ram": "16GB DDR5",
            "storage": "512GB NVMe SSD",
            "display": "15.6-inch FHD 144Hz",
            "battery_hours": 6,
            "weight_lbs": 5.1,
            "os": "Windows 11",
            "gpu": "NVIDIA RTX 4060",
        },
        "summary": "The best budget gaming laptop — RTX 4060 power at under $900.",
        "pros": [
            "RTX 4060 at an aggressive price point",
            "144Hz display for smooth gaming",
            "16GB DDR5 RAM",
        ],
        "cons": [
            "Heavy at 5.1 lbs",
            "Short battery life (6 hours)",
            "Plasticky build quality",
        ],
        "searchable_text": (
            "MSI Katana gaming laptop budget affordable RTX 4060 GPU "
            "gaming AAA games FPS shooter esports 144Hz display "
            "student gamer college cheap gaming powerful graphics"
        ),
    },
    {
        "name": "Samsung Galaxy Book4 Pro 14",
        "category": "laptop",
        "brand": "Samsung",
        "price": 1199.00,
        "image_url": "/products/samsung-galaxy-book4.png",
        "affiliate_url": "https://www.amazon.com/dp/B0CS4GXWT8",
        "specs": {
            "chip": "Intel Core Ultra 7 155H",
            "ram": "16GB LPDDR5",
            "storage": "512GB NVMe SSD",
            "display": "14-inch AMOLED 2.8K",
            "battery_hours": 16,
            "weight_lbs": 2.71,
            "os": "Windows 11",
        },
        "summary": "A stunning AMOLED ultrabook that pairs beautifully with Samsung phones — sleek, light, and vibrant.",
        "pros": [
            "Gorgeous AMOLED display with vivid colors",
            "Super light at 2.71 lbs",
            "Great Samsung ecosystem integration",
            "Long 16-hour battery",
        ],
        "cons": [
            "No dedicated GPU",
            "Samsung bloatware out of the box",
            "Gets warm under load",
        ],
        "searchable_text": (
            "Samsung Galaxy Book AMOLED ultrabook thin light portable beautiful display "
            "Samsung phone ecosystem professional creative travel commute lightweight "
            "vibrant screen premium design work productivity"
        ),
    },

    # ── MORE HEADPHONES ───────────────────────────────────────────────────────
    {
        "name": "Samsung Galaxy Buds3 Pro",
        "category": "headphone",
        "brand": "Samsung",
        "price": 249.99,
        "image_url": "https://image-us.samsung.com/SamsungUS/home/mobile/galaxy-buds/all-galaxy-buds/07102024/Galaxy-Buds3-Pro-White.png",
        "affiliate_url": "https://www.amazon.com/dp/B0D7BHR2T2",
        "specs": {
            "type": "In-ear",
            "anc": True,
            "driver_size_mm": 10.5,
            "battery_hours": 7,
            "battery_with_case_hours": 30,
            "multipoint": True,
            "codec": ["AAC", "SBC", "Samsung Scalable"],
            "water_resistance": "IP57",
        },
        "summary": "The best earbuds for Samsung users — seamless Galaxy integration with solid ANC and great calls.",
        "pros": [
            "Excellent Galaxy ecosystem integration",
            "Strong ANC for earbuds",
            "IP57 dust and water resistant",
            "Crystal-clear call quality",
        ],
        "cons": [
            "Best features locked to Samsung devices",
            "Fit may not suit all ear shapes",
            "No LDAC support",
        ],
        "searchable_text": (
            "Samsung Galaxy Buds earbuds Android Samsung phone ecosystem wireless "
            "ANC noise cancelling workout gym commute everyday portable compact "
            "calls meetings water resistant"
        ),
    },
    {
        "name": "Audio-Technica ATH-M50x",
        "category": "headphone",
        "brand": "Audio-Technica",
        "price": 149.00,
        "image_url": "https://www.audio-technica.com/media/catalog/product/a/t/ath-m50x_01_1.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B00HVLUR86",
        "specs": {
            "type": "Over-ear",
            "anc": False,
            "driver_size_mm": 45,
            "wired": True,
            "foldable": True,
            "impedance_ohms": 38,
        },
        "summary": "The industry-standard studio monitor headphones — detailed, accurate sound trusted by professionals worldwide.",
        "pros": [
            "Studio-reference sound quality",
            "Extremely durable build",
            "Foldable and portable",
            "Detachable cable with 3 options included",
        ],
        "cons": [
            "Wired only — no Bluetooth option",
            "No noise cancellation",
            "Can feel tight after long sessions",
        ],
        "searchable_text": (
            "Audio-Technica ATH-M50x studio monitor wired headphones music production "
            "mixing mastering DJ recording podcasting accurate sound reference "
            "professional durable budget studio affordable closed-back"
        ),
    },
    {
        "name": "JBL Tune 770NC",
        "category": "headphone",
        "brand": "JBL",
        "price": 79.95,
        "image_url": "https://www.jbl.com/dw/image/v2/BFND_PRD/on/demandware.static/-/Sites-masterCatalog_Harman/default/dw5e3fc9ff/JBL_Tune_770NC_Product%20image_Hero_Blue.png",
        "affiliate_url": "https://www.amazon.com/dp/B0CT7BVG79",
        "specs": {
            "type": "Over-ear",
            "anc": True,
            "driver_size_mm": 40,
            "battery_hours": 44,
            "multipoint": True,
            "foldable": True,
        },
        "summary": "The best budget noise-cancelling headphones — incredible value with 44-hour battery and ANC.",
        "pros": [
            "Insanely long 44-hour battery life",
            "ANC at under $80 — great value",
            "JBL bass-forward fun sound",
            "Foldable and lightweight",
        ],
        "cons": [
            "ANC isn't as strong as premium rivals",
            "Plastic build feels cheap",
            "Microphone quality is just okay",
        ],
        "searchable_text": (
            "JBL Tune budget cheap affordable noise cancelling ANC headphones "
            "long battery student school college gym workout commute travel "
            "wireless Bluetooth bass value entry level first headphones"
        ),
    },
    {
        "name": "Sony LinkBuds S",
        "category": "headphone",
        "brand": "Sony",
        "price": 128.00,
        "image_url": "https://www.sony.com/image/da9d99ce45903ad30e31fd6efb2cc891",
        "affiliate_url": "https://www.amazon.com/dp/B09YL76VSR",
        "specs": {
            "type": "In-ear",
            "anc": True,
            "driver_size_mm": 5,
            "battery_hours": 6,
            "battery_with_case_hours": 20,
            "multipoint": True,
            "codec": ["AAC", "SBC", "LDAC"],
            "water_resistance": "IPX4",
        },
        "summary": "Ultra-light ANC earbuds with LDAC hi-res audio — the lightest noise-cancelling buds you can buy.",
        "pros": [
            "Incredibly lightweight — forget you're wearing them",
            "LDAC hi-res audio codec support",
            "Solid ANC for the size",
            "DSEE Extreme upscaling for compressed audio",
        ],
        "cons": [
            "6-hour battery is average",
            "Bass is lighter than competitors",
            "Touch controls can be finicky",
        ],
        "searchable_text": (
            "Sony LinkBuds earbuds lightweight small comfortable all-day wear ANC "
            "noise cancelling LDAC hi-res audio commute office work focus "
            "compact portable gym walking Android iPhone everyday"
        ),
    },
    {
        "name": "Beyerdynamic DT 900 Pro X",
        "category": "headphone",
        "brand": "Beyerdynamic",
        "price": 269.00,
        "image_url": "https://europe.beyerdynamic.com/media/catalog/product/b/e/beyerdynamic-dt-900-pro-x-perspective_transparent.png",
        "affiliate_url": "https://www.amazon.com/dp/B09FLF91S9",
        "specs": {
            "type": "Over-ear",
            "anc": False,
            "driver_size_mm": 45,
            "open_back": True,
            "wired": True,
            "impedance_ohms": 48,
            "frequency_response": "5Hz–40kHz",
        },
        "summary": "Exceptional open-back headphones for audiophiles and studio use — German-engineered sound with velour comfort.",
        "pros": [
            "Wide, precise soundstage for critical listening",
            "Extremely comfortable velour earpads",
            "Easy to drive at 48 ohms",
            "Replaceable parts — built to last decades",
        ],
        "cons": [
            "Open-back — sound leaks in/out",
            "Wired only",
            "Minimal bass for casual listeners",
        ],
        "searchable_text": (
            "Beyerdynamic DT 900 Pro X open-back audiophile studio headphones "
            "mixing mastering critical listening hi-fi music home studio "
            "wired reference accurate German engineering comfortable"
        ),
    },

    # ── MORE CAMERAS ──────────────────────────────────────────────────────────
    {
        "name": "Canon PowerShot V10",
        "category": "camera",
        "brand": "Canon",
        "price": 329.00,
        "image_url": "https://static.bhphoto.com/images/images500x500/canon_5946c001_powershot_v10_vlog_camera_1686225606_1773090.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B0C5DKWCGB",
        "specs": {
            "sensor": "1-inch 20MP",
            "sensor_size": "1-inch",
            "megapixels": 20,
            "video": "4K 30fps",
            "autofocus": "Dual Pixel CMOS AF",
            "stabilization": "Electronic",
            "lens": "Fixed 19mm f/2.8 wide-angle",
            "battery_hours": 1.5,
        },
        "summary": "The simplest vlogging camera — pocket-sized with a built-in stand and one-touch recording.",
        "pros": [
            "Tiny and pocketable",
            "Built-in kickstand for hands-free recording",
            "One-button recording — dead simple",
            "Good 1-inch sensor for the size",
        ],
        "cons": [
            "Short battery life",
            "Fixed wide-angle only — no zoom",
            "No weather sealing",
        ],
        "searchable_text": (
            "Canon PowerShot V10 pocket vlog camera simple easy beginner compact "
            "YouTube TikTok social media one-button recording travel portable "
            "budget affordable first camera starter vlogger content"
        ),
    },
    {
        "name": "DJI Osmo Action 5 Pro",
        "category": "camera",
        "brand": "DJI",
        "price": 349.00,
        "image_url": "https://stormsend1.djicdn.com/tpc/uploads/photos/79581/large_4be5f23f-c3b6-467f-a64a-f3e498d7c32d.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B0DGF8VS4K",
        "specs": {
            "sensor": "1/1.3-inch",
            "megapixels": 40,
            "video": "4K 120fps",
            "stabilization": "RockSteady 3.0+",
            "waterproof_meters": 20,
            "battery_hours": 3.5,
        },
        "summary": "A GoPro rival with superior battery life and deeper waterproofing — great for diving and extreme sports.",
        "pros": [
            "Waterproof to 20m — double the GoPro",
            "Longer 3.5hr battery life",
            "4K 120fps slow motion",
            "Excellent stabilization",
        ],
        "cons": [
            "Smaller accessory ecosystem than GoPro",
            "Touchscreen hard to use when wet",
            "Color science less refined",
        ],
        "searchable_text": (
            "DJI Osmo Action camera adventure sports outdoor waterproof diving "
            "scuba swimming surfing extreme sports action cam POV helmet mount "
            "4K slow motion stabilization long battery"
        ),
    },
    {
        "name": "Sony Alpha a6400",
        "category": "camera",
        "brand": "Sony",
        "price": 898.00,
        "image_url": "https://www.sony.com/image/5d02da5df552836db894cead8a68f5f3",
        "affiliate_url": "https://www.amazon.com/dp/B07MTWVN3M",
        "specs": {
            "sensor": "APS-C 24.2MP",
            "sensor_size": "APS-C",
            "megapixels": 24,
            "video": "4K 30fps",
            "autofocus": "Real-time eye AF",
            "stabilization": "None (lens-dependent)",
            "mount": "Sony E-mount",
            "battery_shots": 410,
        },
        "summary": "A proven workhorse for photo and video — the most popular mirrorless camera for creators on a budget.",
        "pros": [
            "Best-in-class real-time eye autofocus",
            "Massive Sony E-mount lens selection",
            "Compact and lightweight body",
            "Flip-up screen for selfies and vlogging",
        ],
        "cons": [
            "No in-body stabilization",
            "Older menu system",
            "4K recording has a crop",
        ],
        "searchable_text": (
            "Sony a6400 Alpha mirrorless camera creator photographer portrait "
            "eye autofocus vlog YouTube content video photo E-mount lens "
            "compact mid-range reliable popular proven workhorse budget"
        ),
    },
    {
        "name": "Panasonic Lumix S5 IIX",
        "category": "camera",
        "brand": "Panasonic",
        "price": 1999.00,
        "image_url": "https://static.bhphoto.com/images/images500x500/panasonic_dc_s5m2xbody_lumix_dc_s5iix_mirrorless_camera_1686081543_1764706.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B0C37FQVX7",
        "specs": {
            "sensor": "Full-frame 24.2MP",
            "sensor_size": "Full-frame",
            "megapixels": 24,
            "video": "6K 30fps, 4K 120fps",
            "autofocus": "Phase hybrid AF",
            "stabilization": "In-body 5-axis IBIS",
            "mount": "L-mount",
            "battery_shots": 370,
        },
        "summary": "A video powerhouse — unlimited recording, 6K, and pro-grade codecs make this the indie filmmaker's dream.",
        "pros": [
            "Unlimited video recording — no overheating",
            "6K and 4K 120fps for cinematic work",
            "Excellent IBIS stabilization",
            "Full HDMI out for external monitors",
        ],
        "cons": [
            "Autofocus slower than Sony rivals",
            "L-mount lens selection is smaller",
            "Heavier body",
        ],
        "searchable_text": (
            "Panasonic Lumix S5 IIX full-frame video cinema filmmaker indie "
            "filmmaking 6K 4K 120fps slow motion unlimited recording "
            "professional videography documentary wedding video production"
        ),
    },
    {
        "name": "Insta360 X4",
        "category": "camera",
        "brand": "Insta360",
        "price": 499.00,
        "image_url": "https://static.bhphoto.com/images/images500x500/insta360_cinsabma_x4_360_action_camera_1713972600_1826562.jpg",
        "affiliate_url": "https://www.amazon.com/dp/B0D1ML6KL7",
        "specs": {
            "sensor": "1/2-inch dual",
            "megapixels": 72,
            "video": "8K 360° / 4K reframe",
            "stabilization": "FlowState",
            "waterproof_meters": 10,
            "battery_hours": 2.5,
        },
        "summary": "The best 360 camera — shoot everything, then reframe the perfect angle in editing.",
        "pros": [
            "8K 360° capture — never miss a moment",
            "AI reframing creates perfect compositions",
            "Invisible selfie stick effect",
            "Waterproof to 10m",
        ],
        "cons": [
            "Requires editing to get final shots",
            "Image quality below traditional cameras",
            "Short battery life",
        ],
        "searchable_text": (
            "Insta360 X4 360 camera panoramic VR immersive travel adventure "
            "reframe AI editing creative social media unique perspective "
            "action sports skiing snowboarding motorcycle real estate"
        ),
    },
]
