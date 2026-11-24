#!/usr/bin/env python3
"""Render front-page.png for Monday 23 November 2026.

A single 1024x1024 newspaper front page summarising the day's world
news. Every story on the page happened, or was first reported, on
23 November 2026; the sources are listed in README.md. This script is
build-time only -- main.py only copies the finished PNG.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
CREAM = (250, 246, 236)
INK = (22, 22, 22)
NAVY = (16, 38, 66)
GOLD = (203, 164, 44)
CRIMSON = (172, 32, 32)
TEAL = (13, 96, 96)
MUTED = (96, 91, 82)
DIVIDER = (186, 178, 160)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class Sheet:
    """A drawing surface plus the fonts and helpers a front page needs."""

    def __init__(self):
        self.canvas = Image.new("RGB", (PAGE, PAGE), CREAM)
        self.pen = ImageDraw.Draw(self.canvas)
        self.cache = {}

    def typeface(self, path, size):
        key = (path, size)
        if key not in self.cache:
            self.cache[key] = ImageFont.truetype(path, size)
        return self.cache[key]

    def split(self, text, face, width):
        """Greedy word wrap returning a list of lines that fit width."""
        out, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.pen.textlength(trial, font=face) <= width:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def paragraph(self, x, y, text, face, width, colour=INK, gap=None):
        step = gap if gap is not None else int(face.size * 1.24)
        for line in self.split(text, face, width):
            self.pen.text((x, y), line, font=face, fill=colour)
            y += step
        return y

    def rule(self, y, left=24, right=1000, colour=DIVIDER, weight=2):
        self.pen.line([(left, y), (right, y)], fill=colour, width=weight)
        return y

    def feature(self, x, y, width, tag, tag_colour, title, body,
                title_size=20, title_face=None, body_size=15):
        """A kicker line, a bold headline and a short body paragraph."""
        head = title_face or self.typeface(SERIF, title_size)
        self.pen.text((x, y), tag, font=self.typeface(SANS_BOLD, 14),
                      fill=tag_colour)
        y = self.paragraph(x, y + 21, title, head, width,
                           gap=int(title_size * 1.18))
        return self.paragraph(x, y + 5, body,
                              self.typeface(SANS, body_size), width,
                              gap=int(body_size * 1.26))


sheet = Sheet()
pen = sheet.pen

# ---------------------------------------------------------------- masthead
pen.rectangle([0, 0, PAGE, 112], fill=NAVY)
pen.text((512, 10), "THE WORLD", font=sheet.typeface(SERIF, 52),
         fill=(250, 248, 240), anchor="ma")
pen.text((512, 66), "MONDAY 23 NOVEMBER 2026",
         font=sheet.typeface(SANS_BOLD, 27), fill=GOLD, anchor="ma")
pen.text((512, 96),
         "One day's world news, in one image  \u2022  Every story happened or was first reported today",
         font=sheet.typeface(SANS, 14), fill=(198, 204, 214), anchor="ma")

# ------------------------------------------------------------------- lead
pen.text((24, 124), "LEAD  \u2014  LIBYA  \u00b7  UKRAINE",
         font=sheet.typeface(SANS_BOLD, 15), fill=CRIMSON)
lead_head = sheet.typeface(SERIF, 35)
y = sheet.paragraph(24, 146, "Ukraine says it sank a Russian warship off Libya",
                    lead_head, 976, gap=41)
y = sheet.paragraph(24, y + 2,
                    "President Zelenskyy confirmed on Monday that seven Ukrainian naval "
                    "drones sank the corvette Merkury at Benghazi and hit the cargo ship "
                    "MV Angara, which Kyiv says carried Russian arms. Satellite images "
                    "showed the capsized hull.",
                    sheet.typeface(SANS, 17), 976, gap=21)
sheet.rule(y + 8)

# ------------------------------------------------- second row: two items
top2 = y + 20
end_left = sheet.feature(24, top2, 478, "CLIMATE  \u2014  COP31, ANTALYA", TEAL,
              "Climate summit ends with no deal",
              "COP31 closed after a record two days in overtime. The EU and more "
              "than 130 countries rejected a text with no fossil-fuel phase-out; "
              "the UN chief said he was deeply disappointed.", 20)
end_right = sheet.feature(522, top2, 478, "EUROPE  \u2014  SANCTIONS", TEAL,
              "EU proposes its toughest Russia sanctions yet",
              "The Commission's 22nd package would bar about 60 Russian banks "
              "from SWIFT, crack down on crypto networks and list 70 more "
              "shadow-fleet ships.", 20)
row2_bottom = max(end_left, end_right)
sheet.rule(row2_bottom + 10)

# ------------------------------------------------ third row: three items
top3 = row2_bottom + 24
end_a = sheet.feature(24, top3, 312, "NATO  \u2014  POLAND", CRIMSON,
              "NATO sends watch plane to Poland",
              "Three Russian missiles fell in south-east Poland. NATO met in "
              "Brussels and agreed to send an AWACS early-warning aircraft; "
              "Poland did not invoke Article 4.", 19)
end_b = sheet.feature(356, top3, 312, "THE GULF  \u2014  HORMUZ", CRIMSON,
              "Iran vows to fight US blockade",
              "Tehran vowed to use every means against a US naval blockade of "
              "the Strait of Hormuz. Iran says it hit US bases in Bahrain; "
              "Bahrain says a factory burned.", 19)
end_c = sheet.feature(688, top3, 312, "UKRAINE  \u2014  KYIV", CRIMSON,
              "Russian strikes kill at least 15 near Kyiv",
              "Eleven died in Dymer, north of Kyiv, where rescuers pulled a boy "
              "alive from the rubble. Ukraine hit refineries deep in Russia, in "
              "Perm and Rostov.", 19)
row3_bottom = max(end_a, end_b, end_c)
sheet.rule(row3_bottom + 10)

# ------------------------------------------------------- the day in brief
brief_top = row3_bottom + 24
pen.text((24, brief_top), "THE DAY IN BRIEF",
         font=sheet.typeface(SERIF, 22), fill=NAVY)
pen.text((1000, brief_top + 4), "21 more stories from Monday",
         font=sheet.typeface(SANS, 14), fill=MUTED, anchor="ra")
sheet.rule(brief_top + 30, weight=3)

BRIEFS = [
    ("INDONESIA", "Factory fire toll put at 24 dead, about 30 missing in Cikande, west of Jakarta."),
    ("SUDAN", "Drones hit Khartoum, damaging a UN building with staff inside; four killed."),
    ("WEST BANK", "Israel's PM-elect Eisenkot calls settler arson attacks \u201cJewish terrorism\u201d."),
    ("IRAN", "Singer Parastoo Ahmadi is flogged with four of her team in Qom, lawyers say."),
    ("BALTIC", "Finland summons Russia's envoy; Moscow warns Estonia over border closure."),
    ("MARKETS", "Asian tech shares slide further as the AI sell-off deepens; euro inflation 4.0%."),
    ("ASIA", "US lead over China in Asia narrows to its smallest since 2018, Lowy finds."),
    ("MATHS", "Riemann author says the 250,000-page claim was a joke; checks still back it."),
    ("HEALTH", "NHS starts the world's largest AI breast-screening trial, for 700,000 women."),
    ("BANGLADESH", "Dhaka says it will arrest and jail ex-PM Hasina if she returns from India."),
    ("NEPAL", "India offers \u20ac1.4bn to rebuild after August's floods."),
    ("US SPORT", "Oklahoma beats Ole Miss 24-17, ending the Rebels' playoff hopes."),
    ("HUNGARY", "PM Peter Magyar plans a visit to Transcarpathia in Ukraine."),
    ("NIGERIA", "President Tinubu says the presidential villa lost water and power."),
    ("GAZA", "Israeli strike kills a UNRWA worker in Jabalia; 99% of Gaza is contaminated, Oxfam says."),
    ("YEMEN", "Houthis say a Saudi strike on Hodeidah killed 17; the claim is unverified."),
    ("NFL", "49ers crush Vikings 35-10 in Mexico City; Cowboys beat Tennessee 51-30."),
    ("FOOTBALL", "Brentford rout Everton 4-0; Michigan stun unbeaten UCLA in triple overtime."),
    ("LOUISIANA", "An Amtrak train derails after hitting a tractor-trailer."),
    ("TECH", "US presses Nvidia over China chip sales; intel tracked an Nvidia-linked contact, NYT says."),
    ("SOLAR", "JinkoSolar claims a perovskite-silicon cell hit 35.24% efficiency."),
]

tag_face = sheet.typeface(SANS_BOLD, 13)
text_face = sheet.typeface(SANS, 13)
columns = (24, 356, 688)
row_pitch = 47
grid_y = brief_top + 42
for pos, (tag, item) in enumerate(BRIEFS):
    col, row = divmod(pos, 7)
    bx = columns[col]
    by = grid_y + row * row_pitch
    lines = sheet.split(tag + " \u2014 " + item, text_face, 312)
    head = lines[0]
    cut = len(tag) + 3
    lead_in, rest = head[:cut], head[cut:]
    pen.text((bx, by), lead_in, font=tag_face, fill=CRIMSON)
    pen.text((bx + pen.textlength(lead_in, font=tag_face), by), rest,
             font=text_face, fill=INK)
    if len(lines) > 1:
        pen.text((bx, by + 16), lines[1], font=text_face, fill=INK)
    if len(lines) > 2:
        pen.text((bx, by + 32), lines[2], font=text_face, fill=INK)

# ------------------------------------------------------------------ footer
sheet.rule(994)
pen.text((24, 1002),
         "All 27 stories above happened or were first reported on Monday 23 November 2026.",
         font=sheet.typeface(SANS, 13), fill=MUTED)
pen.text((1000, 1002), "Sources: Reuters, AP, BBC, AFP, France 24, RFE/RL, CNBC, NHS",
         font=sheet.typeface(SANS, 13), fill=MUTED, anchor="ra")

sheet.canvas.save("front-page.png", optimize=True)
print("saved front-page.png", sheet.canvas.size)
