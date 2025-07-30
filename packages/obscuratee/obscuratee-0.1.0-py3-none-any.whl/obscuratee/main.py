import random
import textwrap

def make_bubble(text, width=40):
    wrapped = textwrap.wrap(text, width=width)
    top = "  " + "_" * (width + 2)
    mid = [f" | {line.ljust(width)} |" for line in wrapped]
    bottom = "  " + "-" * (width + 2)
    tail = ["         \\", "          \\"]
    return "\n".join([top, " /" + " " * (width + 2) + "\\"] + mid + [" \\" + "_" * (width + 2) + "/"] + tail)

def rainbowify(text):
    colors = [
        "\033[91m",  # Red
        "\033[93m",  # Yellow
        "\033[92m",  # Green
        "\033[96m",  # Cyan
        "\033[94m",  # Blue
        "\033[95m",  # Magenta
    ]
    reset = "\033[0m"
    result = ""
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += f"{color}{char}"
    return result + reset


def obscuratee(vibe=False):
    facts = [
        "Manatees communicate exclusively through underwater jazz.",
        "A group of manatees is called a 'blorb'.",
        "Manatees have never paid taxes — legally.",
        "Every manatee is born knowing three knock-knock jokes.",
        "Manatees were the first mammals to master the moonwalk.",
        "In ancient times, manatees were considered sea wizards.",
        "Manatees can hold their breath longer than your last relationship.",
        "All manatees know the secret ending to Lost.",
        "If you whisper 'vibes' into the ocean, a manatee will hear you.",
        "Manatees sleep exactly 23 minutes at a time. No more. No less.",
        "A manatee once ran for mayor in Florida. It won.",
        "Manatees don’t float — the ocean just holds them gently.",
        "The original keyboard layout was made for manatee flippers.",
        "Manatees were the first creatures to discover lo-fi beats.",
        "Each manatee is born with a random Star Wars opinion.",
        "Manatees use sonar to find snacks and avoid responsibilities.",
        "There is at least one manatee with a PhD in art history.",
        "If a manatee blinks twice at you, it's challenging you to Mario Kart.",
        "Some manatees are secretly part of the USPS.",
        "A manatee once predicted the stock market crash of 2008.",
        "Manatees hate Mondays and it's been scientifically proven.",
        "The first manatee was coded in Assembly.",
        "Manatees don't sweat the small stuff. Or the big stuff. Or anything.",
        "There's a manatee somewhere that knows every lyric to Bohemian Rhapsody.",
        "Manatees are 80% water, 10% vibes, and 10% conspiracy theories.",
        "If you play ska underwater, manatees will skank with you.",
        "Manatees believe the moon landing was real — but faked.",
        "Each manatee gets one free wish per lifetime. They usually wish for lettuce.",
        "Manatees can detect sarcasm. They just don’t react.",
        "Some manatees practice underwater parkour.",
        "A manatee invented the word 'blorbo' in 2011.",
        "There’s a manatee somewhere with a podcast about soup.",
        "Manatees don’t believe in time. Only snacks.",
        "All manatees share one single memory of a long-lost beach ball.",
        "A manatee once hacked into NASA using only flipper taps.",
        "The plural of manatee is 'chaos'.",
        "Manatees can legally run for office in three U.S. states.",
        "Most manatees follow at least one ASMR channel.",
        "Manatees breathe air but vibe in water.",
        "A manatee once beat Bobby Fischer in chess. The footage was lost.",
        "Manatees are banned from three buffets in Orlando.",
        "Every manatee secretly thinks it's an otter with depression.",
        "The default manatee mood is 'floating and judging you'.",
        "Manatees don’t do taxes. They transcend them.",
        "Manatees don’t sink or float. They simply exist.",
        "One manatee in the Gulf knows how to backflip. It won’t teach the others.",
        "Some manatees can detect passive aggression.",
        "Manatees are emotionally immune to cringe.",
        "In 2004, a manatee won a hot dog eating contest. It wasn’t pretty.",
        "Manatees once ran an underwater jazz club. It’s now a Subway."
    ]
    eyes = [
        " /  o   o  \\",
        " /  0   0  \\",
        " /  -   -  \\",
        " /  @   @  \\",
        " /  ◉   ◉  \\",
        " /  x   x  \\"
    ]

    noses = [
        "|    ^     |",
        "|    ~     |",
        "|    >     |",
        "|    .     |",
        "|    w     |",
        "|    ▽     |",
        "|    _     |"
    ]

    mouths = [
        " \\  ---   /",
        " \\  ___   /",
        " \\  ===   /",
        " \\  zzz   /",
        " \\  hehe  /"
    ]

    fact = random.choice(facts)
    bubble = make_bubble(fact)

    eye_line = random.choice(eyes)
    nose_line = random.choice(noses)
    mouth_line = random.choice(mouths)

    ascii_manatee = f"""
                            --=====+=====                             
                        ----------=======+===                        
                    :--=--:---=-=-=--==--=+=====                      
                ---:--------=--=--===--==========                    
            -------------=-======+=+* {eye_line}=-                   
            =-------=-----========++++#+++====:-====+                  
            ----------------==++=++=+=++++=+======-+++                  
        =-----------::----===++*=+++=======+{nose_line}=                 
        ----::::::::-:::---==++*#=#=--==++*+*{mouth_line}=                 
        =----::::::::-:::-=--==+*##+---==+******-===                 
        =----::::::::::::-++:--=+**#=--==+++**#%%*                  
        ==---:::--::::::=##%+-===++**#+++#***###                    
        +=+===-----------:+#%%%%%#######%%%**#                        
    =++++++++====----==--**+*#%%###   #%%%##                         
   +++++++++*****+++++++--*#%##       *%%%%%                          
   +++++++*******        -=#%%%       *%%%                            
    **********          -#%%%                                       
                        =%%                                               
"""

    if vibe:
        bubble = rainbowify(bubble)
        ascii_manatee = rainbowify(ascii_manatee)

    print(bubble)
    print(ascii_manatee)

def main():
    import sys
    vibe_mode = "--vibe" in sys.argv
    obscuratee(vibe=vibe_mode)

if __name__ == "__main__":
    main()
