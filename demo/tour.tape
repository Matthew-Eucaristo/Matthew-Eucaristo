# Record with: vhs demo/tour.tape   (from this repo's root, with the tool repos in ../dev-tools)
# Each tool runs from its committed HEAD in its own demo/setup.sh workspace; see demo/tour.sh.
# Afterwards shrink the palette as AGENTS.md describes (keeps the GIF under 1 MB).
Output assets/tour.gif
Set Shell bash
Set FontSize 14
Set Width 1200
Set Height 460
Set Padding 16
Set TypingSpeed 40ms
Set Framerate 10

Hide
Type "source demo/tour.sh && stage fell" Enter
Wait@120s /^\$ *$/
# Start on a full screen, so the GIF's first frame is never an empty terminal.
Type "clear && fell --dry-run" Enter
Wait+Screen@30s /rebuildable/
Sleep 500ms
Show
Sleep 2s
Down Sleep 1s
Down Sleep 1.2s
Type "q"

Hide
Type "exit" Enter
Type "stage flutterkill" Enter
Wait@120s /^\$ *$/
Type "clear" Enter
Sleep 300ms
Show
Type "flutterkill --dry-run" Sleep 300ms Enter
Sleep 3s
Down Sleep 1.2s
Tab Sleep 2s
Type "q"

Hide
Type "exit" Enter
Type "stage nodekill" Enter
Wait@180s /^\$ *$/
Type "clear" Enter
Sleep 300ms
Show
Type "nodekill --dry-run" Sleep 300ms Enter
Sleep 3.5s
Type "s" Sleep 2.5s
Type "q"

Hide
Type "exit" Enter
Type "stage decruft" Enter
Wait@180s /^\$ *$/
# Skip the scan animation: show decruft once its overview is complete.
Type "clear && decruft --dry-run" Enter
Wait+Screen@90s /removable here/
Sleep 2s
Show
Sleep 2.5s
Enter Sleep 2.5s
Down Sleep 1.5s
Type "q"

Hide
Type "exit" Enter
Type "stage lately" Enter
Wait@120s /^\$ *$/
Type "clear" Enter
Sleep 300ms
Show
Type "lately --replay sample" Sleep 300ms Enter
Sleep 2.2s
Down Sleep 200ms
Down Sleep 200ms
Down Sleep 200ms
Down Sleep 600ms
Enter Sleep 2.8s
Type "q"

Hide
Type "exit" Enter
Sleep 3s
