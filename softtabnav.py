import sublime
import sublime_plugin

class SofttabnavCommand(sublime_plugin.TextCommand):
    def run(self, edit, isleft, shift):
        tabsize = self.view.settings().get('tab_size')
        sel = self.view.sel()

        # Region/point storage
        regions = []
        # Loop through selections
        for r in sel:
            # If something is selected and shift-mod is not used, move cursor to
            # selection boundary corresponding with the key press.
            if shift == False and r.a != r.b:
                if isleft:
                    regions.append(r.begin())
                else:
                    regions.append(r.end())
                continue

            pos = r.b
 
            lnregion = self.view.line(pos)
            # Calculate the new selection boundaries and extract the text between old and new bounds
            if isleft:
                target = lnregion.begin() + (pos - lnregion.begin() - 1) // tabsize * tabsize 
                before = sublime.Region(min(lnregion.begin(), pos - 1), pos)
                txt = self.view.substr(before)
            else:
                target = lnregion.begin() + (pos - lnregion.begin() + tabsize) // tabsize * tabsize
                after = sublime.Region(lnregion.begin(), min(lnregion.end(), target))
                txt = self.view.substr(after)

            if txt != ''.ljust(len(txt)):
                target = pos + 1 - 2 * isleft

            if shift:
                # Check if selection origin (r.a) is between target and r.b
                if ((r.a < target and r.a > r.b) or (r.a > target and r.a < r.b)):
                    regions.append(r.a)
                else:
                    regions.append(sublime.Region(r.a, target))                
            else:
                regions.append(target)
                
        sel.clear()
        sel.add_all(regions)
