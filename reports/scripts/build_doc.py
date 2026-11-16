import sys
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

S = sys.argv[1]
OUT = sys.argv[2]
FB = S + "/fb"
YT = S + "/yt"

doc = Document()
st = doc.styles["Normal"]
st.font.name = "Calibri"
st.font.size = Pt(10.5)
for sec in doc.sections:
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin = sec.bottom_margin = Cm(1.8)

NAVY = RGBColor(0x0B, 0x2A, 0x4A)


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hexcolor)
    tcPr.append(sh)


def h(text, lvl=1):
    p = doc.add_heading(text, level=lvl)
    for r in p.runs:
        r.font.color.rgb = NAVY
    return p


def para(text, bold=False, italic=False, size=None):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    return p


def bullets(items, style="List Bullet"):
    for it in items:
        p = doc.add_paragraph(style=style)
        if isinstance(it, tuple):
            p.add_run(it[0]).bold = True
            p.add_run(it[1])
        else:
            p.add_run(it)


def table(header, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, txt in enumerate(header):
        c = t.rows[0].cells[i]
        c.text = ""
        r = c.paragraphs[0].add_run(txt)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        shade(c, "0B2A4A")
    for row in rows:
        cells = t.add_row().cells
        for i, txt in enumerate(row):
            cells[i].text = str(txt)
    t.autofit = False
    if widths:
        for i, gc in enumerate(t._tbl.tblGrid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(int(widths[i] * 567)))
        for i, col in enumerate(t.columns):
            col.width = Cm(widths[i])
    for row in t.rows:
        for i, c in enumerate(row.cells):
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(9.5)
            if widths:
                c.width = Cm(widths[i])
    doc.add_paragraph()
    return t


def image(path, width_cm, caption):
    doc.add_picture(path, width=Cm(width_cm))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c = para(caption, italic=True, size=9)
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER


# ---------- Title ----------
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.LEFT
r = t.add_run("Video Analysis Report")
r.bold = True
r.font.size = Pt(24)
r.font.color.rgb = NAVY
para("Two sources: a Facebook Reel (fully analysed) and a YouTube safety video (provisional, access blocked)", size=12)
para("Date of analysis: 15 November 2026   |   Classification: Internal   |   Status: Part A final, Part B provisional", size=9.5, italic=True)

# ---------- Sources ----------
h("1. Sources and status")
table(
    ["#", "Source", "Link", "Status", "Evidence obtained"],
    [
        ["A", "Facebook Reel, \"AI with PI\"", "facebook.com/share/r/1Dao65knZy", "Complete",
         "Video file, audio, 24 frames + 8 full-res key frames, Whisper transcript, metadata"],
        ["B", "YouTube, IMCA \"Protect your eyes\"", "youtu.be/5MXjKj6SDQ8", "Provisional",
         "Title, channel and thumbnail only. Video and audio not obtained (YouTube bot check)"],
    ],
    widths=[0.8, 3.5, 4, 2.2, 6.5],
)

# ---------- Exec summary ----------
h("2. Executive summary")
bullets([
    ("Source A is a 23.6-second promotional reel. ",
     "A creator claims Claude cannot open social-media videos on its own and promotes a third-party skill called \"Agent Reach\" "
     "that downloads the video, after which Claude studies it frame by frame and critiques the editing. The reel is a teaser for a 3:28 YouTube video."),
    ("The core claim is partly true. ",
     "In this analysis, Claude retrieved and analysed the same reel without that skill, using a standard open-source downloader (yt-dlp), "
     "ffmpeg and a local Whisper model, once network access was granted. The real limit is network policy and platform bot checks, not Claude itself."),
    ("Main risk for a security reader: ",
     "the post encourages users to let an AI agent install tools from a pasted link (\"you don't even have to install them yourself\"). "
     "That is an unvetted-code supply-chain risk and should not be done on corporate devices without review."),
    ("Source B could not be analysed. ",
     "YouTube returned \"Sign in to confirm you're not a bot\" to the cloud server. Metadata confirms it is an IMCA "
     "(International Marine Contractors Association) safety video on eye protection. Section 6 lists what is needed to finish it."),
])

# ---------- Method ----------
h("3. Method and evidence tags")
bullets([
    "Acquisition: yt-dlp 2026.10.26 for video, metadata (info.json) and thumbnails. YouTube oEmbed API for Source B metadata.",
    "Technical profile: ffprobe (codecs, resolution, frame rate) and ffmpeg volumedetect (loudness).",
    "Visual: 1 frame per second (24 frames), scene-change detection (threshold 0.3), 8 key frames read at full 1080x1920 resolution.",
    "Audio: faster-whisper \"small\" model, run locally on CPU with voice-activity filtering. No third-party AI service was used.",
    "Verification: burned-in captions compared word by word against the Whisper transcript. On-screen card text read at full resolution before quoting.",
])
para("Evidence tags used in this report:", bold=True)
table(
    ["Tag", "Meaning"],
    [
        ["[AUDIO mm:ss]", "Heard in the soundtrack, from the Whisper transcript"],
        ["[FRAME mm:ss]", "Seen in an extracted video frame"],
        ["[CAPTION]", "Burned-in on-screen caption text"],
        ["[META]", "Platform metadata (title, channel, dates, counts)"],
        ["[INFERRED]", "Analyst judgement, not directly stated in the video"],
        ["[UNVERIFIED]", "Claim made in the video that this analysis could not confirm"],
    ],
    widths=[3.5, 13.5],
)

# ---------- Part A ----------
h("4. Part A: Facebook Reel")
h("4.1 Metadata and technical profile", 2)
table(
    ["Field", "Value", "Tag"],
    [
        ["Page / creator", "AI with PI", "[META]"],
        ["Video ID", "1798030111423651", "[META]"],
        ["Upload date", "13 November 2026", "[META]"],
        ["Duration", "23.6 s", "[META] / ffprobe"],
        ["Engagement", "Title text shows \"111K views, 1.1K reactions\". The API field returned 44,613 views. The figures differ, likely counting different surfaces.", "[META]"],
        ["Post text", "\"I let Claude edit my whole video. Cuts, captions, graphics, even the sound effects. All you need is 2 free tools: FFmpeg + HyperFrames... just paste the link and Claude sets them up.\"", "[META]"],
        ["Hashtags", "#claude #aivideoediting #aitools #contentcreator #ffmpeg #aiwithpi", "[META]"],
        ["Video", "AV1, 1080x1920 (9:16 vertical), 30 fps, ~630 kbps", "ffprobe"],
        ["Audio", "AAC stereo, 48 kHz, ~82 kbps. Mean -16.7 dB, peak -1.7 dB (loud, no clipping)", "ffmpeg"],
        ["Language", "English (Whisper confidence 0.97)", "[AUDIO]"],
    ],
    widths=[3.2, 11.3, 2.5],
)

h("4.2 Full transcript", 2)
table(
    ["Time", "Spoken words", "Tag"],
    [
        ["00:00-00:06", "\"I can use another skill, it's called Agent Reach, because normally you cannot get videos directly through Claude.\"", "[AUDIO]"],
        ["00:06-00:15", "\"So after Claude got the video, Claude will split it out frames by frames, study the whole clips and then give you the result.\"", "[AUDIO]"],
        ["00:15-00:22", "\"It also able to analyze the clip and know which one look well, which one look good and look bad and how to implement into your own videos.\"", "[AUDIO]"],
        ["00:22-00:24", "\"...videos on my YouTube.\" (cut off at the end)", "[AUDIO]"],
    ],
    widths=[2.5, 12.5, 2],
)
para("Caption check: the burned-in captions match the audio word for word (e.g. \"BECAUSE NORMALLY / GET VIDEOS / DIRECTLY THROUGH\", "
     "\"OUT FRAME / BY FRAME / STUDY THE / WHOLE CLIP\"). No mislabelled or altered captions were found. [CAPTION] vs [AUDIO]", italic=True, size=9.5)

h("4.3 Visual timeline", 2)
para("Scene changes detected at 2.97 s, 5.90 s, 8.80 s, 14.90 s and 17.03 s. Layout throughout: a top graphic panel over a talking-head shot, with bold word-by-word captions at the bottom.")
table(
    ["Time", "What is on screen", "Tag"],
    [
        ["00:00-00:03", "Hook card: \"here's the fix / CLAUDE CAN'T OPEN REELS\" (\"CAN'T\" highlighted yellow). Presenter in glasses, seated indoors, hand gestures.", "[FRAME]"],
        ["00:03-00:06", "Card \"AGENT REACH: a free skill that downloads the video for Claude\". Mock terminal line changes from \"facebook.com/reel/... Claude can't open this\" (red) to \"reel.mp4 downloaded\" (green). Platform tags: Facebook, YouTube, Instagram. Footer at 00:05: \"No skill? Download the video yourself and drop it in.\"", "[FRAME 00:04, 00:05]"],
        ["00:06-00:09", "Full-screen talking head, no graphic.", "[FRAME]"],
        ["00:09-00:15", "Card \"FRAME BY FRAME / AI FILM ANALYSIS: Claude studies the reference frame by frame\". A filmstrip of another creator's reel scrolls with a playhead (frames labelled 0:00 to 0:12). Small print notes the reference is shown blurred, at 1 frame per second.", "[FRAME 00:10] [small print partly legible]"],
        ["00:15-00:17", "Close-up talking head with \"AI FILM ANALYSIS\" tag.", "[FRAME]"],
        ["00:17-00:21", "Analysis cards: \"0:00 HOOK: her real tool on screen + one huge keyword on frame 1\" (tick), \"0:11 BRANDING: 'THIS VIDEO · CLAUDE EDIT' sticker + a tiny mascot\" (tick), \"DON'T COPY: her robot looks like Claude Code's own mascot\" (red cross). Then \"IN MY EDIT: 'CLAUDE EDITED THIS' + our own Clapper Pi, on frame 1\".", "[FRAME 00:17-00:21]"],
        ["00:22-00:24", "End card: \"the whole edit · 3:28 / FULL VIDEO ON YOUTUBE\".", "[FRAME 00:22]"],
    ],
    widths=[2.3, 12.2, 2.5],
)
image(f"{FB}/sheet_1.jpg", 16.5, "Figure 1. Frames 00:00 to 00:11 at 1 fps (timestamps top left).")
image(f"{FB}/sheet_2.jpg", 16.5, "Figure 2. Frames 00:12 to 00:23 at 1 fps.")
image(f"{FB}/cards.jpg", 8, "Figure 3. Full-resolution crops of the text cards at 00:04, 00:19, 00:20 and 00:21.")

h("4.4 Claim check", 2)
table(
    ["Claim", "Verdict", "Evidence"],
    [
        ["\"Claude can't open reels\" / \"normally you cannot get videos directly through Claude\"",
         "Partly true",
         "Claude has no built-in video player. But in this analysis Claude fetched the reel with yt-dlp and analysed it once the cloud network allowed Facebook's hosts. The limit is network policy and platform bot checks. [INFERRED from this session's logs]"],
        ["Agent Reach is \"a free skill that downloads the video for Claude\"",
         "Unverified",
         "No source, repo link or publisher shown in the reel. Not tested here. [UNVERIFIED]"],
        ["Claude splits the video \"frame by frame\" and studies it",
         "Supported",
         "This is the method used in this report (ffmpeg frame extraction, then visual review). [INFERRED]"],
        ["Claude can judge which edits \"look good and look bad\"",
         "Supported with caveat",
         "Claude can describe and critique composition, pacing and captions. Judgements of \"good\" are subjective and depend on the brief. [INFERRED]"],
        ["Post text: \"just paste the link and Claude sets them up\"",
         "True but risky",
         "Agents can install tools on request. Doing so from an unvetted link runs third-party code with the agent's permissions. [INFERRED]"],
    ],
    widths=[5, 2.5, 9.5],
)

h("4.5 Production and persuasion techniques", 2)
bullets([
    ("Problem-first hook: ", "a negative claim (\"CLAUDE CAN'T\") in the first frame stops the scroll, then \"here's the fix\" promises the answer."),
    ("Word-by-word captions: ", "large white captions with one yellow keyword per beat. Most reels are watched muted, so these carry the message."),
    ("Proof cards: ", "mock terminal output (red fail, green success) gives a quick before-and-after."),
    ("Teardown format: ", "ticks and crosses on another creator's video, which reads as expert critique."),
    ("Clear call to action: ", "the end card sends viewers to the 3:28 YouTube video."),
    ("Pacing: ", "6 visual segments in 24 seconds, about one change every 4 seconds."),
])

h("4.6 Security and governance observations", 2)
bullets([
    ("Supply-chain risk: ", "installing an unnamed \"skill\" or tools via a pasted link lets third-party code run on the user's machine or cloud session. Review the source, publisher and permissions first. [INFERRED]"),
    ("Content rights: ", "the reel analyses another creator's video (shown blurred). Downloading third-party content for analysis should respect platform terms and copyright, especially in a corporate setting. [INFERRED]"),
    ("Data handling: ", "for sensitive footage (CCTV, incidents), run transcription locally as done here, rather than sending it to a third-party AI service. [INFERRED]"),
    ("Brand use: ", "the creator notes a third party's mascot resembles Claude Code's mascot and advises \"don't copy\", a fair trademark caution. [FRAME 00:20]"),
])

# ---------- Part B ----------
h("5. Part B: YouTube video (provisional)")
para("This section is PROVISIONAL. The video and audio could not be retrieved, so nothing below describes the video's content beyond its metadata and thumbnail.", bold=True)
table(
    ["Field", "Value", "Tag"],
    [
        ["Title", "Protect your eyes", "[META]"],
        ["Channel", "IMCA (@IMCAint), International Marine Contractors Association", "[META]"],
        ["Video ID", "5MXjKj6SDQ8", "[META]"],
        ["Thumbnail", "IMCA logo, \"BE PREPARED TO WORK SAFELY / Protect your eyes\". A worker on a vessel deck in a white hard hat, safety glasses and orange hi-vis coveralls, leaning on the rail with the sea behind.", "[FRAME thumbnail]"],
        ["Duration, transcript, scenes", "Not obtained", "-"],
    ],
    widths=[3.5, 11, 2.5],
)
image(f"{YT}/thumb.jpg", 6.5, "Figure 4. YouTube thumbnail (only visual evidence available for Source B).")
para("Likely subject (to confirm): this appears to be part of IMCA's \"Be prepared to work safely\" awareness series on eye protection in offshore and marine work. "
     "Expect topics such as eye hazards (flying particles, chemicals, UV, welding arc), correct PPE selection and wear, and emergency eyewash. [INFERRED, not verified]", italic=True)

h("Why it was blocked", 2)
bullets([
    "YouTube's metadata host was reachable, but the video request returned \"Sign in to confirm you're not a bot\". YouTube applies this to cloud server IP addresses.",
    "Four standard player clients were tried and all hit the same check. Tactics that disguise the request were not used, as that would route around YouTube's access control.",
])

# ---------- Next steps ----------
h("6. Next steps to complete Part B")
bullets([
    ("Option 1 (fastest): ", "download the video on your own device (YouTube Premium offline, or IMCA's own site if they host it) and upload the .mp4 to this session. Analysis takes about 10 minutes from upload."),
    ("Option 2: ", "send the video's captions. On YouTube: open the video, \"...\" menu, Show transcript, copy and paste. I can then write the full audio section, with visuals limited to the thumbnail."),
    ("Option 3: ", "run this session's toolchain on your own computer via Remote Control, where your home or office IP is not bot-checked."),
], style="List Number")

h("7. Limitations")
bullets([
    "Whisper \"small\" model: accurate for clear English speech, but may miss words under music. The final words at 00:22 were cut off in the source.",
    "Small-print text at 00:09-00:15 is only partly legible even at full resolution.",
    "View counts differ between Facebook surfaces (111K in the title vs 44,613 from the API).",
    "\"Agent Reach\" was not tested and its publisher was not identified.",
])

h("Appendix: environment changes made for this task")
para("A personal cloud environment \"command-centre-video\" was created with access to: youtube.com, youtu.be, i.ytimg.com, facebook.com (www, m), "
     "three Facebook video CDN hosts (video-ord5-1/-2.xx.fbcdn.net, scontent-ord5-2.xx.fbcdn.net) and Hugging Face model hosts for Whisper. "
     "Facebook CDN host names can change by region. If a future reel fails, the exact blocked host is added the same way.", size=9.5)

doc.save(OUT)
print("saved", OUT)
