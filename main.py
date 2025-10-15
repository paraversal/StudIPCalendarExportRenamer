import sys
import ics
import os
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Input, Button
from textual.containers import Vertical
from textual import events
from rich.text import Text
from textual import on

class Event():
    def __init__(self, event_name: str) -> None:
        self.original_event_name: str = event_name
        self.final_event_name: str = event_name
        self.is_merge_candidate: bool = False

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Event):
            return self.final_event_name == value.final_event_name
        else:
            return False

    def __hash__(self) -> int:
       return hash(self.final_event_name)
        

class Model():
    def __init__(self, unique_events: dict[str, str]):
        self.events = [Event(event) for event in unique_events]
        self.cursor_position = 0
        self.is_renaming: bool = False

class CalendarRenamer(App):
    CSS = """
    Input {
        margin: 2 4;
    }
    DataTable {
        margin: 2 4;
    }

    """
   
    BINDINGS = [
        ("m", "toggle_merge", "Add/Remove from merge"), 
        ("r", "rename", "Rename"), 
        ("M", "merge", "Merge")
        ]
    
    async def action_quit(self) -> None:
        event_mapping = {event.original_event_name:event.final_event_name for event in model.events}
        for event in calendar.events:
            event.name = event_mapping[event.name]
        with open("renamed_events.ics", "w") as f:
            f.writelines(calendar.serialize_iter())
        self.app.exit()

    def get_displayed_events(self) -> list[Event]:
        seen = set()
        unique = []
        for e in model.events:
            if e.final_event_name not in seen:
                seen.add(e.final_event_name)
                unique.append(e)
        return unique


    def action_toggle_merge(self):
        displayed = self.get_displayed_events()
        cursor_row, _ = self.datatable.cursor_coordinate

        if cursor_row < 0 or cursor_row >= len(displayed):
            return

        rep = displayed[cursor_row]
        
        current_state = any(
            (e.is_merge_candidate for e in model.events if e.final_event_name == rep.final_event_name)
        )
        new_state = not current_state
        
        for e in model.events:
            if e.final_event_name == rep.final_event_name:
                e.is_merge_candidate = new_state

        model.cursor_position = cursor_row
        self.update_table()

        if len([candidate for candidate in model.events if candidate.is_merge_candidate]) > 1:
            self.input.placeholder = "Rename group (r)"

    def action_merge(self):
        merge_candidates = [candidate for candidate in model.events if candidate.is_merge_candidate]
        if len(merge_candidates) < 2:
            return
        # simply choose the first event as the one to keep
        for candidate in merge_candidates[1:]:
            model.events.remove(candidate)
        merge_candidates[0].is_merge_candidate = False
        self.update_table()
        
    def action_rename(self):
        self.input.disabled = False
        self.input.focus()

    @on(Input.Submitted)
    def input_submitted(self):
        if self.input.value == "":
            return

        merge_candidates = [candidate for candidate in model.events if candidate.is_merge_candidate]
        if len(merge_candidates) == 0:
            displayed = self.get_displayed_events()
            cursor_row, _ = self.datatable.cursor_coordinate
            if cursor_row < len(displayed):
                rep = displayed[cursor_row]
                previous_name = rep.final_event_name
                target_name = self.input.value
                for e in model.events:
                    if e.final_event_name == previous_name:
                        e.final_event_name = target_name
                        e.is_merge_candidate = False
        else:
            new_name = self.input.value
            for candidate in merge_candidates:
                old_name = candidate.final_event_name
                for e in model.events:
                    if e.final_event_name == old_name:
                        e.final_event_name = new_name
                        e.is_merge_candidate = False

        self.input.value = ""
        self.input.placeholder = "Rename event to... (r)"
        self.input.disabled = True
        self.update_table()

    def compose(self) -> ComposeResult:
        self.datatable = DataTable(zebra_stripes=True, show_header=False)
        self.input = Input(disabled=True, placeholder="Rename event to... (r)")

        with Vertical():
            yield Header()
            yield self.datatable
            yield self.input
            yield Footer()

    def update_table_size(self, new_width: int)-> None:
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.add_column("event", width=new_width-10)
        self.update_table()

    def update_table(self) -> None:
        table = self.query_one(DataTable)
        table.clear()

        for event in self.get_displayed_events():
            style = ""
            if event.is_merge_candidate:
                style = "bold underline on magenta"
            else:
                style = ""
            text = Text(str(event.final_event_name), justify="center")
            text.stylize(style)

            table.add_row(
                text,
                height=None,  # Use None to auto-detect the optimal height.
            )
        table.move_cursor(row=model.cursor_position)

    def on_resize(self, event: events.Resize) -> None:
        self.update_table_size(event.size.width)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        raise Exception("Usage: uv run main.py -- <file path to calendar export>")
    with open(sys.argv[1], "r") as f:
        content = f.read()
    calendar = ics.Calendar(content)

    all_event_names = [event.name for event in calendar.events]
    unique_events = set(all_event_names)
    event_to_event = {event:event for event in unique_events} 

    model = Model(event_to_event)
    app = CalendarRenamer()
    app.run()
