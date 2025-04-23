import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

TASKS_FILE = "tasks.json"

class ToDoApp(App):
    def build(self):
        self.load_tasks()

        self.layout = BoxLayout(orientation="vertical")
        self.task_input = TextInput(hint_text="Enter a task", size_hint=(1, 0.1))
        self.layout.add_widget(self.task_input)
        
        self.add_button = Button(text="Add Task", size_hint=(1, 0.1))
        self.add_button.bind(on_press=self.add_task)
        self.layout.add_widget(self.add_button)
        
        self.task_list = BoxLayout(orientation="vertical", size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.scroll_view.add_widget(self.task_list)
        self.layout.add_widget(self.scroll_view)
        
        self.display_tasks()
        
        return self.layout
    
    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []
    
    def save_tasks(self):
        with open(TASKS_FILE, "w") as file:
            json.dump(self.tasks, file)
    
    def add_task(self, instance):
        task_text = self.task_input.text.strip()
        if task_text:
            self.tasks.append({"task": task_text, "completed": False})
            self.task_input.text = ""
            self.save_tasks()
            self.display_tasks()
    
    def display_tasks(self):
        self.task_list.clear_widgets()
        for index, task in enumerate(self.tasks):
            self.task_list.add_widget(self.create_task_widget(index, task))
    
    def create_task_widget(self, index, task):
        task_layout = BoxLayout(size_hint_y=None, height=40)
        task_label = Label(text=task["task"], size_hint_x=0.7, color=(0, 1, 0, 1) if task["completed"] else (1, 1, 1, 1))
        
        complete_button = Button(text="✔" if task["completed"] else "Mark Done", size_hint_x=0.15)
        complete_button.bind(on_press=lambda x: self.mark_complete(index))
        
        delete_button = Button(text="❌", size_hint_x=0.15)
        delete_button.bind(on_press=lambda x: self.delete_task(index))
        
        task_layout.add_widget(task_label)
        task_layout.add_widget(complete_button)
        task_layout.add_widget(delete_button)
        
        return task_layout
    
    def mark_complete(self, index):
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_tasks()
        self.display_tasks()
    
    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.display_tasks()

if __name__ == "__main__":
    ToDoApp().run()
