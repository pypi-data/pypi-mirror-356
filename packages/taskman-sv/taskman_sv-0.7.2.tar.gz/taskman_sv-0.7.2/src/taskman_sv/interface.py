import os
import time
import msvcrt
import tempfile
import subprocess
from tqdm import tqdm
from colorama import Fore, Style, init
from datetime import datetime, date, timedelta
import sys
import time
import itertools
from .taskman_backend import setup_backend, TaskmanBackend
import json

# Create a global backend instance
backend = TaskmanBackend()

# Initialize colorama
init(autoreset=True)

try:
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
except ImportError:
    engine = None

tasks = []  # List to store tasks
notes = {}  # Dictionary to store modular notes
quick_notes = []  # List to store quick notes
paused_task = None
current_progress = 0

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def welcome_banner():
    """Display welcome banner with TASKMAN info and features before login"""
    clear_screen()
    
    # Original TASKMAN logo with right-aligned attribution
    logo = f"""{Fore.GREEN}
  ████████╗ █████╗ ███████╗██╗  ██╗███╗   ███╗ █████╗ ███╗   ██╗
  ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝████╗ ████║██╔══██╗████╗  ██║
     ██║   ███████║███████╗█████╔╝ ██╔████╔██║███████║██╔██╗ ██║
     ██║   ██╔══██║╚════██║██╔═██╗ ██║╚██╔╝██║██╔══██║██║╚██╗██║
     ██║   ██║  ██║███████║██║  ██╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Fore.YELLOW}                                                                📦 Part of The Hard Club Suite {Fore.YELLOW}(www.thehardclub.com)
{Fore.LIGHTYELLOW_EX}                                                                             Created by Shreedhar{Style.RESET_ALL}
    """
    
    print(logo)
    
    # Original features display (unchanged)
    features = f"""{Fore.CYAN}🌟 TASKMAN - Your Personal Task Management Assistant 🌟
{Fore.GREEN}✨ Core Features:
{Fore.WHITE}• 🎯 Task Management
  ├─ ⚡ Custom Tasks with Smart Timer
  └─ 🍅 {Fore.LIGHTRED_EX}Pomodoro Technique™{Fore.WHITE} with Flexible Sessions

{Fore.WHITE}• 🧠 Focus Modes
  ├─ 🚀 HyperFocus Mode with Real-time Tracking
  └─ 🎮 Normal Mode with Enhanced UI

{Fore.WHITE}• 📊 Progress & Analytics
  ├─ 📈 Daily Progress Tracking
  └─ 📑 Detailed Reports Generation

{Fore.WHITE}• 📝 Notes System
  ├─ 📘 Modular Notes with Categories
  └─ ⚡ Quick Notes for Rapid Capture

{Fore.LIGHTBLUE_EX}💡 Pro Tip: {Fore.YELLOW}Type '?' anytime for detailed help menu  {Fore.CYAN}            [Press Enter to begin your productive journey⚡🚀✨...]{Style.RESET_ALL}"""

    print(features)
    time.sleep(1.5)
    input()

def loading_animation():
    """Display a professional loading animation with a Matrix-style effect"""
    logo = f"""{Fore.GREEN}
  ████████╗ █████╗ ███████╗██╗  ██╗███╗   ███╗ █████╗ ███╗   ██╗
  ╚══██╔══╝██╔══██╗██╔════╝██║ ██╔╝████╗ ████║██╔══██╗████╗  ██║
     ██║   ███████║███████╗█████╔╝ ██╔████╔██║███████║██╔██╗ ██║
     ██║   ██╔══██║╚════██║██╔═██╗ ██║╚██╔╝██║██╔══██║██║╚██╗██║
     ██║   ██║  ██║███████║██║  ██╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
{Fore.WHITE}                                                              by Shreedhar
    """
    
    print(logo)
    display_features()  # Add features display after logo
    time.sleep(1.5)

def display_features():
    """Display TASKMAN features during startup"""
    features = f"""{Fore.CYAN}🌟 TASKMAN - Your Personal Task Management Assistant 🌟
{Fore.GREEN}✨ Core Features:
{Fore.WHITE}• 🎯 Task Management
  ├─ ⚡ Custom Tasks with Smart Timer
  └─ 🍅 {Fore.LIGHTRED_EX}Pomodoro Technique™{Fore.WHITE} with Flexible Sessions

{Fore.WHITE}• 🧠 Focus Modes
  ├─ 🚀 HyperFocus Mode with Real-time Tracking
  └─ 🎮 Normal Mode with Enhanced UI

{Fore.WHITE}• 📊 Progress & Analytics
  ├─ 📈 Daily Progress Tracking
  └─ 📑 Detailed Reports Generation

{Fore.WHITE}• 📝 Notes System
  ├─ 📘 Modular Notes with Categories
  └─ ⚡ Quick Notes for Rapid Capture

{Fore.LIGHTBLUE_EX}💡 Pro Tip: {Fore.YELLOW}Type '?' anytime for detailed help menu  {Fore.CYAN}            [Press Enter to begin your productive journey⚡🚀✨...]{Style.RESET_ALL}"""

    
    print(features)
    input()

def calculate_daily_stats():
    """Calculate daily statistics for display"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    total_worked = 0
    completed_count = 0
    pending_count = 0
    time_remaining = 0
    
    for task in tasks:
        # Only count today's tasks or carry-forward tasks
        task_date = task.get('creation_date', today)
        
        if "Completed" in task['status']:
            completed_count += 1
            # Use actual time worked if available, otherwise use progress
            if 'actual_time_worked' in task and task['actual_time_worked'] > 0:
                total_worked += task['actual_time_worked']
            elif task.get('mode') == 'pomodoro' and 'pomodoro_history' in task:
                # For Pomodoro tasks without actual_time_worked, calculate from history
                settings = task.get('pomodoro_settings', {})
                completed_pomodoros = len(task['pomodoro_history'])
                work_duration = settings.get('work_duration', 25)  # Default 25 minutes
                total_worked += completed_pomodoros * work_duration * 60
            elif 'duration' in task:
                total_worked += task['duration']
        else:
            pending_count += 1
            # Calculate remaining time for pending tasks
            if task.get('mode') == 'pomodoro':
                # For Pomodoro tasks, calculate remaining based on completed vs total Pomodoros
                settings = task.get('pomodoro_settings', {})
                completed_pomodoros = len(task.get('pomodoro_history', []))
                total_pomodoros = settings.get('num_pomodoros', 0)
                remaining_pomodoros = max(0, total_pomodoros - completed_pomodoros)
                work_duration = settings.get('work_duration', 25)
                time_remaining += remaining_pomodoros * work_duration * 60
                
                # Also add to total_worked if there are completed Pomodoros
                if completed_pomodoros > 0:
                    total_worked += completed_pomodoros * work_duration * 60
            elif 'remaining' in task:
                time_remaining += task['remaining']
            else:
                time_remaining += task.get('duration', 0)
    
    return {
        'total_worked': total_worked,
        'completed_count': completed_count, 
        'pending_count': pending_count,
        'time_remaining': time_remaining
    }

def format_time_duration(seconds):
    """Format seconds into readable time string"""
    # Convert to int to ensure no decimal points in display
    seconds = int(seconds)
    
    if seconds == 0:
        return "0m"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def display_header(title="TASKMAN", module=None):
    """Clears the screen and displays the title at the top before the date."""
    clear_screen()
    
    # Get current hour to determine greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # Display greeting with username if available
    if hasattr(backend, 'user') and backend.user:
        print(f"\n{Fore.GREEN}{greeting}, {backend.user}! 👋")
    
    if module:
        print(f"\n{Fore.CYAN}🌟 {title} - {Fore.GREEN}{module} 🌟\n")
    else:
        print(f"\n{Fore.CYAN}🌟 {title} 🌟")
    
    today = datetime.now().strftime("%A, %d %B %Y")
    print(f"{Fore.CYAN}📅 {today}")
    print()  # Add space between date and stats
    
    # Calculate and display daily statistics
    stats = calculate_daily_stats()
    
    # Format the statistics with colors and icons
    worked_time = format_time_duration(stats['total_worked'])
    remaining_time = format_time_duration(stats['time_remaining'])
    
    stats_line = (
        f"{Fore.LIGHTBLUE_EX}📊 Today: "
        f"{Fore.CYAN}⏱️ Worked {Fore.WHITE}{worked_time} {Fore.CYAN}| "
        f"{Fore.GREEN}✅ Completed {Fore.WHITE}{stats['completed_count']} {Fore.CYAN}| "
        f"{Fore.YELLOW}⏳ Pending {Fore.WHITE}{stats['pending_count']} {Fore.CYAN}| "
        f"{Fore.MAGENTA}🎯 Remaining {Fore.WHITE}{remaining_time}"
        f"{Style.RESET_ALL}"
    )
    
    print(stats_line)
    print()  # Add extra spacing

def get_time_input():
    while True:
        try:
            hours = input("Enter estimated hours (0-23): ")
            if hours.strip() == "":
                return None, None
            hours = int(hours)
            if 0 <= hours <= 23:
                break
            print("\033[A\033[K")  # Clear previous line
            print("Please enter a number between 0 and 23")
        except ValueError:
            print("\033[A\033[K")  # Clear previous line
            print("Please enter a valid number")
    
    while True:
        try:
            minutes = input("Enter estimated minutes (0-59): ")
            if minutes.strip() == "":
                return None, None
            minutes = int(minutes)
            if 0 <= minutes <= 59:
                break
            print("\033[A\033[K")  # Clear previous line
            print("Please enter a number between 0 and 59")
        except ValueError:
            print("\033[A\033[K")  # Clear previous line
            print("Please enter a valid number")
    
    return hours, minutes

def display_tasks():
    """Display all tasks including paused ones"""
    if tasks:
        print(f"{Fore.BLUE}📝 Active Tasks:")
        for i, task in enumerate(tasks, 1):
            hrs = task['duration'] // 3600 if 'duration' in task else 0
            mins = (task['duration'] % 3600) // 60 if 'duration' in task else 0
            status = task['status']
            
            # Add task type badge with updated colors
            if task['mode'] == 'custom':
                badge = f"{Fore.CYAN}[🛠️]"
            else:  # pomodoro
                badge = f"{Fore.LIGHTRED_EX}[🍅 POMO]"
            
            # Check if task has a creation date and it's from a previous day
            creation_date = task.get('creation_date', datetime.now().strftime('%Y-%m-%d'))
            today = datetime.now().strftime('%Y-%m-%d')
            carryforward_info = ""
            if creation_date != today:
                carryforward_info = f"{Fore.YELLOW}[↻ from {creation_date}] "
            
            # Display task with badge, number, name, duration, status and carryforward info
            if task['mode'] == 'custom':
                print(f"{badge} {i}. {carryforward_info}{task['name']} [{hrs}h {mins}m] - {status}")
            else:
                settings = task['pomodoro_settings']
                total = settings.get('num_pomodoros', 0)
                
                # Check if task is completed - if so, show all pomodoros as completed
                if "Completed" in task['status']:
                    completed = total
                else:
                    # For active tasks, use current_pomodoro or pomodoro_history length
                    completed = max(
                        settings.get('current_pomodoro', 0),
                        len(task.get('pomodoro_history', []))
                    )
                
                print(f"{badge} {i}. {carryforward_info}{task['name']} [{completed}/{total} Pomodoros] - {status}")
            
            if task['description']:
                print(f"   Description: {task['description']}")
            print("   ────────────────────────────────────────")
    else:
        print(f"{Fore.YELLOW}No active tasks! Add some first.")
    print()

def speak(text):
    """Simple voice announcement"""
    if not engine:
        return
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"{Fore.RED}Voice error: {str(e)}")

def get_task_type():
    while True:
        print("\nTask Type:")
        print("1. Custom Task")
        print("2. Pomodoro Task")
        print("3. Back to Main Menu")
        
        # Colored input prompt using magenta
        choice = input(f"\n{Fore.MAGENTA}Choose option (1/2/3): {Style.RESET_ALL}")
        
        if choice == "1":
            return "custom"
        elif choice == "2":
            return "pomodoro"
        elif choice == "3":
            return "back"
        else:
            print("\033[A\033[K")  # Clear previous line
            print("Please enter a valid option (1, 2, or 3)")

def get_valid_time_input(prompt):
    """Get valid time input from user"""
    while True:
        try:
            value = input(f"{Fore.CYAN}{prompt}")
            if not value.strip():
                return None
            value = int(value)
            if value <= 0:
                print(f"{Fore.YELLOW}Please enter a positive number.")
                continue
            return value
        except ValueError:
            print(f"{Fore.YELLOW}Please enter a valid number.")

def add_task():
    task_type = get_task_type()
    if task_type == "back":
        return
    
    # Get common task details
    name = input(f"\n{Fore.CYAN}Enter task name: ").strip()
    while not name:
        print(f"{Fore.YELLOW}Task name cannot be empty.")
        name = input(f"{Fore.CYAN}Enter task name: ").strip()
    
    description = input(f"{Fore.CYAN}Enter a brief description: ").strip()
    while not description:
        print(f"{Fore.YELLOW}Description cannot be empty.")
        description = input(f"{Fore.CYAN}Enter a brief description: ").strip()
    
    # Handle different task types
    if task_type == "custom":
        # Get duration
        hours, minutes = get_time_input()
        if hours is None or minutes is None:
            return
        
        total_seconds = hours * 3600 + minutes * 60
        task_mode = "custom"
        
    elif task_type == "pomodoro":
        print(f"\n{Fore.CYAN}Pomodoro Settings:")
        print(f"{Fore.YELLOW}1. Standard (25min work, 5min break, 15min long break)")
        print(f"{Fore.YELLOW}2. Long (45min work, 15min break, 30min long break)")
        print(f"{Fore.YELLOW}3. Custom Pomodoro")
        
        pomo_type = input(f"\n{Fore.CYAN}Choose Pomodoro type (1/2/3): ").strip()
        
        if pomo_type == "1":
            work_duration = 25
            break_duration = 5
            long_break_duration = 15
        elif pomo_type == "2":
            work_duration = 45
            break_duration = 15
            long_break_duration = 30
        elif pomo_type == "3":
            work_duration = get_valid_time_input("Work duration (minutes): ")
            break_duration = get_valid_time_input("Break duration (minutes): ")
            long_break_duration = get_valid_time_input("Long break duration (minutes): ")
        else:
            print(f"{Fore.RED}Invalid choice. Using standard Pomodoro settings.")
            work_duration = 25
            break_duration = 5
            long_break_duration = 15
        
        num_pomodoros = get_valid_time_input("Number of Pomodoros: ")
        if num_pomodoros is None:
            return
        
        total_seconds = (work_duration * 60 * num_pomodoros) + \
                       (break_duration * 60 * (num_pomodoros - 1)) + \
                       (long_break_duration * 60)  # One long break at the end
        
        task_mode = "pomodoro"
    
    # Show summary and get confirmation
    print(f"\n{Fore.GREEN}Task Summary:")
    print(f"{Fore.CYAN}Name: {Fore.WHITE}{name}")
    print(f"{Fore.CYAN}Description: {Fore.WHITE}{description}")
    
    if task_type == "custom":
        hrs = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        print(f"{Fore.CYAN}Duration: {Fore.WHITE}{hrs}h {mins}m")
    else:
        print(f"{Fore.CYAN}Pomodoro Settings:")
        print(f"{Fore.WHITE}  Work Duration: {work_duration}min")
        print(f"{Fore.WHITE}  Break Duration: {break_duration}min")
        print(f"{Fore.WHITE}  Long Break Duration: {long_break_duration}min")
        print(f"{Fore.WHITE}  Number of Pomodoros: {num_pomodoros}")
        print(f"{Fore.WHITE}  Total Duration: {total_seconds//3600}h {(total_seconds%3600)//60}m")
    
    confirm = input(f"\n{Fore.YELLOW}Is this correct? (y/n): ").lower()
    if confirm == 'y':
        task_data = {
            "name": name,
            "description": description,
            "duration": total_seconds,
            "status": f"{Fore.YELLOW}Pending",
            "mode": task_mode,
            "creation_date": datetime.now().strftime('%Y-%m-%d'),
            "actual_time_worked": 0,  # Track real work time
            "work_sessions": []  # Track individual work periods
        }
        
        # Add Pomodoro-specific data if applicable
        if task_mode == "pomodoro":
            task_data.update({
                "pomodoro_settings": {
                    "work_duration": work_duration,
                    "break_duration": break_duration,
                    "long_break_duration": long_break_duration,
                    "num_pomodoros": num_pomodoros,
                    "current_pomodoro": 0
                }
            })
        
        tasks.append(task_data)
        print(f"{Fore.GREEN}» Task added! ✅")

def edit_task(task_index):
    """Edit an existing task's details"""
    try:
        task = tasks[task_index-1]
    except IndexError:
        print(f"{Fore.RED}Invalid task number!")
        return

    while True:
        clear_screen()
        print(f"\n{Fore.GREEN}Current Task Details:")
        print(f"{Fore.CYAN}1. Name: {Fore.WHITE}{task['name']}")
        print(f"{Fore.CYAN}2. Description: {Fore.WHITE}{task['description']}")
        
        hours = task['duration'] // 3600
        minutes = (task['duration'] % 3600) // 60
        print(f"{Fore.CYAN}3. Duration: {Fore.WHITE}{hours}h {minutes}m")
        print(f"{Fore.CYAN}4. Status: {task['status']}")
        
        print(f"\n{Fore.YELLOW}What would you like to edit?")
        
        # Show different options based on task status
        if "Completed" in task['status']:
            print(f"{Fore.YELLOW}1. Name")
            print(f"{Fore.YELLOW}2. Description")
            print(f"{Fore.YELLOW}3. Save and Exit")
            valid_choices = ['1', '2', '3']
        else:
            print(f"{Fore.YELLOW}1. Name")
            print(f"{Fore.YELLOW}2. Description")
            print(f"{Fore.YELLOW}3. Duration")
            print(f"{Fore.YELLOW}4. Save and Exit")
            valid_choices = ['1', '2', '3', '4']
        
        choice = input(f"\n{Fore.GREEN}Choice (1-{len(valid_choices)}): ").strip()
        
        if choice not in valid_choices:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)
            continue
        
        if choice == '1':
            new_name = input(f"{Fore.CYAN}Enter new name: ").strip()
            while not new_name:
                print(f"{Fore.YELLOW}Name cannot be empty.")
                new_name = input(f"{Fore.CYAN}Enter new name: ").strip()
            task['name'] = new_name
            print(f"{Fore.GREEN}» Name updated!")
            time.sleep(1)
        
        elif choice == '2':
            new_desc = input(f"{Fore.CYAN}Enter new description: ").strip()
            while not new_desc:
                print(f"{Fore.YELLOW}Description cannot be empty.")
                new_desc = input(f"{Fore.CYAN}Enter new description: ").strip()
            task['description'] = new_desc
            print(f"{Fore.GREEN}» Description updated!")
            time.sleep(1)
        
        elif choice == '3' and "Completed" not in task['status']:
            try:
                print(f"{Fore.CYAN}Current duration: {hours}h {minutes}m")
                while True:
                    try:
                        new_hours = int(input(f"{Fore.CYAN}Enter new hours: "))
                        if new_hours < 0:
                            print(f"{Fore.YELLOW}Hours cannot be negative.")
                            continue
                        if new_hours > 24:
                            confirm = input(f"{Fore.YELLOW}Are you sure you want to set {new_hours} hours? (y/n): ").lower()
                            if confirm != 'y':
                                continue
                        
                        new_minutes = int(input(f"{Fore.CYAN}Enter new minutes: "))
                        if new_minutes < 0 or new_minutes >= 60:
                            print(f"{Fore.YELLOW}Minutes must be between 0 and 59.")
                            continue
                        break
                    except ValueError:
                        print(f"{Fore.YELLOW}Please enter valid numbers.")
                
                task['duration'] = new_hours * 3600 + new_minutes * 60
                
                # Update remaining time if task is paused
                if "Paused" in task['status'] and 'remaining' in task:
                    task['remaining'] = task['duration']
                
                print(f"{Fore.GREEN}» Duration updated!")
                time.sleep(1)
            except ValueError:
                print(f"{Fore.RED}Please enter valid numbers!")
                time.sleep(1)
        
        elif (choice == '4' and "Completed" not in task['status']) or \
             (choice == '3' and "Completed" in task['status']):
            break
    
    backend.save_tasks(tasks)
    print(f"{Fore.GREEN}» Task updated successfully! ✅")
    time.sleep(1)

def hyperfocus_mode(task, current_progress=0):
    """Display task in HyperFocus mode with enhanced visuals"""
    global current_mode
    current_mode = "hyperfocus"
    
    # Define cool nerd emojis for transition
    focus_emojis = ["🧠", "⚡", "🎯", "💡", "🚀", "🔬", "🎮", "⌨️", "🖥️"]
    emoji_index = 0
    
    clear_screen()
    print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
    print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
    print(f"{Fore.LIGHTCYAN_EX}Description: {Fore.WHITE}{task['description']}\n")
    
    total = task['duration']
    original_duration = total  # Store original duration
    
    # Calculate actual progress for paused tasks
    if 'remaining' in task:
        current_progress = original_duration - task['remaining']
        total = task['remaining']
    
    print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
    
    try:
        with tqdm(total=original_duration, desc=f"{Fore.LIGHTCYAN_EX}Progress", 
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] " + focus_emojis[emoji_index],
                ascii="▰▱") as pbar:
            
            pbar.update(current_progress)
            start_time = time.time() - current_progress
            elapsed_start = time.time()
            spoken_halfway = current_progress >= (original_duration // 2)
            last_emoji_update = time.time()
            
            while pbar.n < original_duration:
                try:
                    # Update emoji every 0.4 seconds instead of 3
                    current_time = time.time()
                    if current_time - last_emoji_update >= 0.1:  # Changed from 0.4 to 0.1
                        emoji_index = (emoji_index + 1) % len(focus_emojis)
                        # Remove the vertical line by using a space before the emoji
                        pbar.bar_format = "{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] " + focus_emojis[emoji_index]
                        last_emoji_update = current_time
                    
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = original_duration - pbar.n
                            task['remaining'] = remaining
                            task['status'] = f"{Fore.YELLOW}⏸ Paused"
                            task['pause_start_time'] = time.time()
                            task['paused_progress'] = pbar.n  # Store exact progress when paused
                            speak("Task paused")
                            
                            # Show pause screen
                            pause_action = pause_screen(task, pbar.n, original_duration, "hyperfocus")
                            if pause_action == "resume":
                                task['status'] = f"{Fore.BLUE}In Progress"
                                # Set new start_time based on current time minus paused progress
                                start_time = time.time() - task['paused_progress']
                                clear_screen()
                                print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
                                print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
                                print(f"{Fore.LIGHTCYAN_EX}Description: {Fore.WHITE}{task['description']}\n")
                                print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
                                continue
                            elif pause_action == "completed":
                                return "completed", original_duration
                            elif pause_action == "main_menu":
                                return "paused", pbar.n
                        elif key == b'b':  # Back to normal mode
                            return "normal", pbar.n
                        elif key == b'n':  # Notes
                            temp_progress = pbar.n
                            notes_interface(backend)
                            clear_screen()
                            print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
                            print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
                            print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
                        elif key == b'f':  # FastNotes
                            temp_progress = pbar.n
                            fast_notes_interface(backend)
                            clear_screen()
                            print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE ACTIVATED 🌟\n")
                            print(f"{Fore.LIGHTCYAN_EX}Task: {Fore.LIGHTGREEN_EX}{task['name']}")
                            print(f"{Fore.YELLOW}Commands: [N]otes | [F]astNotes | [B]ack to Normal Mode | [P]ause\n")
                except Exception as e:
                    # Debug: Show any exceptions that occur
                    print(f"\n{Fore.RED}Debug - Exception in HyperFocus: {str(e)}")
                    time.sleep(1)

                current_time = time.time()
                pbar.n = int(current_time - start_time)
                pbar.last_print_n = pbar.n - 1
                pbar.refresh()
                
                if pbar.n >= original_duration // 2 and not spoken_halfway:
                    print(f"\n{Fore.LIGHTCYAN_EX}🎉 Halfway Completed! 💪")
                    speak("Halfway Completed!")
                    spoken_halfway = True

        task['status'] = f"{Fore.GREEN}Completed ✅"
        task['end_time'] = datetime.now().strftime('%H:%M:%S')
        
        # Track actual work time
        if 'actual_time_worked' not in task:
            task['actual_time_worked'] = 0
        if 'work_sessions' not in task:
            task['work_sessions'] = []
        
        # Add this session's work time
        task['actual_time_worked'] += original_duration
        task['work_sessions'].append({
            'duration': original_duration,
            'mode': 'hyperfocus',
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"\n{Fore.LIGHTGREEN_EX}✨ Task Completed Successfully! ✨")
        speak("Task Completed Successfully!")
        return "completed", original_duration
            
    except KeyboardInterrupt:
        task['status'] = f"{Fore.RED}Interrupted ⚠️"
        print(f"\n{Fore.RED}Task interrupted!")
        speak("Task interrupted")
        return "interrupted", 0

def normal_task_mode(task, current_progress=0):
    """Original task mode with progress bar"""
    global current_mode
    current_mode = "normal"
    
    clear_screen()
    display_header()
    display_tasks()
    
    total = task['duration']
    original_duration = total  # Store original duration
    task['status'] = f"{Fore.BLUE}In Progress"
    
    # Calculate actual progress for paused tasks
    if 'remaining' in task:
        current_progress = original_duration - task['remaining']
        total = task['remaining']
    
    spoken_halfway = current_progress >= (original_duration // 2)
    
    print(f"\n{Fore.GREEN}🚀 Starting: {task['name']} ({total//3600}h {total%3600//60}m)")
    print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")

    # When starting the task
    task['start_time'] = datetime.now().strftime('%H:%M:%S')

    try:
        with tqdm(total=original_duration, desc=f"{Fore.CYAN}Countdown", 
                bar_format="{l_bar}%s{bar}%s| {n_fmt}/{total_fmt}" % (Fore.GREEN, Fore.RESET)) as pbar:
            
            pbar.update(current_progress)
            start_time = time.time() - current_progress
            initial_elapsed = current_progress
            elapsed_start = time.time() - initial_elapsed
            
            while pbar.n < original_duration:
                try:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = original_duration - pbar.n
                            task['remaining'] = remaining
                            task['status'] = f"{Fore.YELLOW}⏸ Paused"
                            task['pause_start_time'] = time.time()
                            task['paused_progress'] = pbar.n  # Store exact progress when paused
                            speak("Task paused")
                            
                            # Show pause screen
                            pause_action = pause_screen(task, pbar.n, original_duration, "normal")
                            if pause_action == "resume":
                                task['status'] = f"{Fore.BLUE}In Progress"
                                # Set new start_time based on current time minus paused progress
                                start_time = time.time() - task['paused_progress']
                                elapsed_start = time.time() - task['paused_progress']  # Reset elapsed_start too
                                clear_screen()
                                display_header()
                                display_tasks()
                                print(f"\n{Fore.GREEN}🚀 Resuming: {task['name']}")
                                print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")
                                continue
                            elif pause_action == "completed":
                                return "completed", original_duration
                            elif pause_action == "main_menu":
                                return "paused", pbar.n
                        elif key == b'h':  # Switch to HyperFocus
                            return "hyper", pbar.n
                        elif key == b'n':  # Notes
                            temp_progress = pbar.n
                            notes_interface(backend)
                            clear_screen()
                            display_header()
                            display_tasks()
                            print(f"\n{Fore.GREEN}🚀 Resuming: {task['name']}")
                            print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")
                        elif key == b'f':  # FastNotes
                            temp_progress = pbar.n
                            fast_notes_interface(backend)
                            clear_screen()
                            display_header()
                            display_tasks()
                            print(f"\n{Fore.GREEN}🚀 Resuming: {task['name']}")
                            print(f"{Fore.YELLOW}Press 'N' for Notes, 'F' for FastNotes, 'P' to Pause, 'H' for HyperFocus\n")
                except Exception as e:
                    # Debug: Show any exceptions that occur
                    print(f"\n{Fore.RED}Debug - Exception in Normal Mode: {str(e)}")
                    time.sleep(1)

                current_time = time.time()
                pbar.n = int(current_time - start_time)
                pbar.last_print_n = pbar.n - 1
                pbar.refresh()
                
                # Add halfway completion announcement
                if pbar.n >= original_duration // 2 and not spoken_halfway:
                    print(f"\n{Fore.CYAN} Halfway Completed! 💪")
                    speak("Halfway Completed!")
                    spoken_halfway = True
                
                elapsed = int(current_time - elapsed_start)
                elapsed_mins, elapsed_secs = divmod(elapsed, 60)
                remaining = original_duration - pbar.n
                mins, secs = divmod(remaining, 60)
                pbar.set_description(f"{Fore.CYAN}Remaining: {mins:02d}:{secs:02d} [{elapsed_mins:02d}:{elapsed_secs:02d}]")
                time.sleep(0.1)

        # When completing the task
        task['status'] = f"{Fore.GREEN}Completed ✅"
        task['end_time'] = datetime.now().strftime('%H:%M:%S')
        
        # Track actual work time
        if 'actual_time_worked' not in task:
            task['actual_time_worked'] = 0
        if 'work_sessions' not in task:
            task['work_sessions'] = []
        
        # Add this session's work time
        task['actual_time_worked'] += original_duration
        task['work_sessions'].append({
            'duration': original_duration,
            'mode': 'normal',
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"\n{Fore.GREEN}✨ Task Completed Successfully! ✨")
        speak("Task Completed Successfully!")
        return "completed", original_duration
            
    except KeyboardInterrupt:
        task['status'] = f"{Fore.RED}Interrupted ⚠️"
        print(f"\n{Fore.RED}Task interrupted!")
        speak("Task interrupted")
        return "interrupted", pbar.n

def pomodoro_mode(task):
    """Dedicated Pomodoro mode with specialized UI and functionality"""
    clear_screen()
    settings = task['pomodoro_settings']
    current_pomodoro = settings['current_pomodoro']
    total_pomodoros = settings['num_pomodoros']
    
    # Initialize start time if not exists
    if 'start_time' not in task:
        task['start_time'] = datetime.now().strftime('%H:%M:%S')
    
    # Initialize pomodoro history if not exists
    if 'pomodoro_history' not in task:
        task['pomodoro_history'] = []
    
    # Initialize pause state if not exists
    if 'paused_state' not in task:
        task['paused_state'] = {
            'phase': 'work',
            'time_left': 0,
            'current_pomodoro': current_pomodoro
        }
    
    def display_pomodoro_header():
        clear_screen()
        print(f"\n{Fore.MAGENTA}🍅 POMODORO MODE 🍅\n")
        print(f"{Fore.CYAN}Task: {Fore.GREEN}{task['name']}")
        print(f"{Fore.CYAN}Description: {Fore.WHITE}{task['description']}")
        print(f"{Fore.CYAN}Started at: {Fore.WHITE}{task['start_time']}\n")
        
        # Display completed Pomodoros history with progress bars
        if task['pomodoro_history']:
            print(f"{Fore.YELLOW}Completed Pomodoros:")
            for i, pomo in enumerate(task['pomodoro_history'], 1):
                print(f"{Fore.WHITE}  #{i}: {pomo['timestamp']} - Work: {pomo['work_duration']}min")
                # Show completed work session bar
                print(f"{Fore.GREEN}  Work Time: 100%|{'▰' * 50}| {settings['work_duration']*60}/{settings['work_duration']*60}")
                # Show completed break bar if it's not the last Pomodoro
                if i < total_pomodoros:
                    print(f"{Fore.BLUE}  Break Time: 100%|{'▰' * 50}| {settings['break_duration']*60}/{settings['break_duration']*60}\n")
        print()
        
        print(f"{Fore.YELLOW}Session Settings:")
        print(f"Work Duration: {settings['work_duration']} minutes")
        print(f"Break Duration: {settings['break_duration']} minutes")
        print(f"Long Break Duration: {settings['long_break_duration']} minutes")
        print(f"Progress: {current_pomodoro}/{total_pomodoros} Pomodoros\n")
        print(f"{Fore.YELLOW}Commands: [P]ause | [Q]uit\n")
    
    def display_current_session(phase, progress_bars):
        """Display current session with history"""
        clear_screen()
        display_pomodoro_header()
        
        # Display completed progress bars
        for bar in progress_bars:
            print(bar)
        
        if phase == 'work':
            print(f"\n{Fore.GREEN}🍅 Starting Pomodoro {current_pomodoro + 1}/{total_pomodoros}")
        elif phase == 'break':
            print(f"\n{Fore.BLUE}☕ Starting Break ({settings['break_duration']} minutes)")
    
    def handle_pause_state():
        """Handle paused state using the same pause screen as other modes"""
        phase = task['paused_state']['phase']
        time_left = task['paused_state']['time_left']
        
        # Calculate current progress and original duration based on phase
        if phase == 'work':
            original_duration = settings['work_duration'] * 60
            current_progress = original_duration - time_left
        else:  # break
            if current_pomodoro < total_pomodoros:
                break_duration = settings['break_duration']
            else:
                break_duration = settings['long_break_duration']
            original_duration = break_duration * 60
            current_progress = original_duration - time_left
        
        # Use the same pause screen as other modes
        pause_action = pause_screen(task, current_progress, original_duration, "pomodoro")
        
        if pause_action == "resume":
            return "resume"
        elif pause_action == "completed":
            return "completed"
        elif pause_action == "main_menu":
            task['status'] = f"{Fore.YELLOW}⏸ Paused"
            return "main_menu"

    try:
        while current_pomodoro < total_pomodoros:
            display_pomodoro_header()
            
            # Work Session
            print(f"\n{Fore.GREEN}🍅 Starting Pomodoro {current_pomodoro + 1}/{total_pomodoros}")
            work_seconds = settings['work_duration'] * 60
            
            # Resume from pause if applicable
            paused_state = task.get('paused_state', {})
            if paused_state.get('phase') == 'work' and paused_state.get('time_left', 0) > 0:
                work_seconds = paused_state.get('time_left', work_seconds)
                print(f"{Fore.YELLOW}Resuming work session...")
            
            with tqdm(total=settings['work_duration'] * 60, 
                     initial=settings['work_duration'] * 60 - work_seconds,
                     desc=f"{Fore.GREEN}Work Time", 
                     bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                     ascii="▰▱") as pbar:
                
                start_time = time.time()
                end_time = start_time + work_seconds
                
                while time.time() < end_time:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = end_time - time.time()
                            task['paused_state'] = {
                                'phase': 'work',
                                'time_left': remaining,
                                'current_pomodoro': current_pomodoro
                            }
                            pause_result = handle_pause_state()
                            if pause_result == "resume":
                                # If we continue, update the end time
                                end_time = time.time() + remaining
                            elif pause_result == "completed":
                                return "completed"
                            elif pause_result == "main_menu":
                                task['status'] = f"{Fore.YELLOW}⏸ Paused"
                                return "main_menu"
                        elif key == b'q':  # Quit
                            task['pomodoro_settings']['current_pomodoro'] = current_pomodoro
                            return "quit"
                    
                    pbar.n = settings['work_duration'] * 60 - int(end_time - time.time())
                    pbar.refresh()
                    time.sleep(0.1)
            
            # After work session completes
            current_pomodoro += 1
            task['pomodoro_settings']['current_pomodoro'] = current_pomodoro
            
            # Record completed Pomodoro
            task['pomodoro_history'].append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'work_duration': settings['work_duration']
            })
            
            speak("Work session complete")
            print(f"\n{Fore.GREEN}✨ Work session complete!")
            time.sleep(1)
            
            # Break session
            if current_pomodoro < total_pomodoros:
                break_duration = settings['break_duration']
                break_type = "Break"
            else:
                break_duration = settings['long_break_duration']
                break_type = "Long Break"
            
            print(f"\n{Fore.BLUE}☕ Starting {break_type} ({break_duration} minutes)")
            break_seconds = break_duration * 60
            
            # Check if resuming from break pause before setting new pause state
            paused_state = task.get('paused_state', {})
            if paused_state.get('phase') == 'break' and paused_state.get('time_left', 0) > 0:
                break_seconds = paused_state.get('time_left', break_seconds)
                print(f"{Fore.YELLOW}Resuming break...")
            else:
                # Only set new pause state if not resuming
                task['paused_state'] = {
                    'phase': 'break',
                    'time_left': break_seconds,
                    'current_pomodoro': current_pomodoro
                }
            
            with tqdm(total=break_duration * 60,
                     initial=break_duration * 60 - break_seconds,
                     desc=f"{Fore.BLUE}{break_type}", 
                     bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
                     ascii="▰▱") as pbar:
                
                start_time = time.time()
                end_time = start_time + break_seconds
                
                while time.time() < end_time:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().lower()
                        if key == b'p':  # Pause
                            remaining = end_time - time.time()
                            task['paused_state'] = {
                                'phase': 'break',
                                'time_left': remaining,
                                'current_pomodoro': current_pomodoro
                            }
                            pause_result = handle_pause_state()
                            if pause_result == "resume":
                                # If we continue, update the end time
                                end_time = time.time() + remaining
                            elif pause_result == "completed":
                                return "completed"
                            elif pause_result == "main_menu":
                                task['status'] = f"{Fore.YELLOW}⏸ Paused"
                                return "main_menu"
                        elif key == b'q':  # Quit
                            task['pomodoro_settings']['current_pomodoro'] = current_pomodoro
                            return "quit"
                    
                    pbar.n = break_duration * 60 - int(end_time - time.time())
                    pbar.refresh()
                    time.sleep(0.1)
            
            # Reset pause state for next work session
            task['paused_state'] = {
                'phase': 'work',
                'time_left': settings['work_duration'] * 60,
                'current_pomodoro': current_pomodoro
            }
            
            speak("Break complete")
            print(f"\n{Fore.GREEN}✨ Break complete!")
            time.sleep(1)
        
        # All Pomodoros completed
        task['status'] = f"{Fore.GREEN}Completed ✅"
        task['end_time'] = datetime.now().strftime('%H:%M:%S')
        task['paused_state'] = None  # Clear pause state when completed
        
        # Track actual work time for completed Pomodoros
        if 'actual_time_worked' not in task:
            task['actual_time_worked'] = 0
        if 'work_sessions' not in task:
            task['work_sessions'] = []
        
        # Calculate actual work time from completed Pomodoros
        total_work_time = len(task['pomodoro_history']) * settings['work_duration'] * 60
        task['actual_time_worked'] += total_work_time
        task['work_sessions'].append({
            'duration': total_work_time,
            'mode': 'pomodoro_completed',
            'timestamp': datetime.now().isoformat(),
            'pomodoros_completed': len(task['pomodoro_history'])
        })
        
        print(f"\n{Fore.GREEN}🎉 All Pomodoros completed successfully!")
        speak("All Pomodoros completed successfully")
        return "completed"
            
    except KeyboardInterrupt:
        task['status'] = f"{Fore.RED}Interrupted ⚠️"
        print(f"\n{Fore.RED}Pomodoro interrupted!")
        speak("Pomodoro interrupted")
        return "interrupted"

def start_task(task_index):
    """Enhanced start_task function with HyperFocus mode support"""
    global current_progress, current_mode
    
    try:
        task = tasks[task_index-1]
    except IndexError:
        print(f"{Fore.RED}Invalid task number!")
        return

    if "Completed" in task['status']:
        print(f"{Fore.YELLOW}This task is already completed! 🎉")
        return

    # Initialize current_progress based on whether it's a resumed task
    if 'remaining' in task:
        current_progress = task['duration'] - task['remaining']
    else:
        current_progress = 0

    if task['mode'] == 'pomodoro':
        status = pomodoro_mode(task)
        backend.save_tasks(tasks)
        return

    # Ask for mode selection
    print(f"\n{Fore.CYAN}Select Mode:")
    print(f"{Fore.YELLOW}1. Normal Mode")
    print(f"{Fore.MAGENTA}2. HyperFocus Mode")
    mode = input(f"\n{Fore.GREEN}Choose mode (1/2): ").strip()

    while True:  # Continue running until task is completed or interrupted
        if mode == "2":
            status, progress = hyperfocus_mode(task, current_progress)
        else:
            status, progress = normal_task_mode(task, current_progress)
        
        # Update current_progress based on the returned progress
        current_progress = progress
        
        # Handle different status returns
        if status == "completed" or status == "interrupted" or status == "paused":
            # Reset current_progress after task completion/interruption
            current_progress = 0
            # Clear the remaining time if task is completed
            if status == "completed" and 'remaining' in task:
                del task['remaining']
            break
        elif status == "normal":
            mode = "1"  # Switch to normal mode
            # Update remaining time based on current progress
            task['remaining'] = task['duration'] - current_progress
            continue
        elif status == "hyper":
            mode = "2"  # Switch to hyperfocus mode
            # Update remaining time based on current progress
            task['remaining'] = task['duration'] - current_progress
            continue

def resume_task():
    """Prompts user for task number and resumes the paused task"""
    paused_tasks = [(i, task) for i, task in enumerate(tasks, 1) if "Paused" in task['status']]
    
    if not paused_tasks:
        print(f"{Fore.YELLOW}No paused tasks to resume!")
        return
    
    print(f"\n{Fore.CYAN}Paused tasks:")
    for i, task in paused_tasks:
        if task['mode'] == 'pomodoro':
            # Show Pomodoro-specific progress
            settings = task['pomodoro_settings']
            completed_pomodoros = len(task.get('pomodoro_history', []))
            total_pomodoros = settings.get('num_pomodoros', 0)
            remaining_pomodoros = total_pomodoros - completed_pomodoros
            
            if remaining_pomodoros > 0:
                if remaining_pomodoros == 1:
                    progress_text = "1 Pomodoro remaining"
                else:
                    progress_text = f"{remaining_pomodoros} Pomodoros remaining"
            else:
                progress_text = "All Pomodoros completed"
                
            print(f"{Fore.MAGENTA}{i}. {task['name']} ({progress_text})")
        else:
            # Show time remaining for custom tasks
            remaining_mins = int(task.get('remaining', 0)) // 60
            remaining_secs = int(task.get('remaining', 0)) % 60
            print(f"{Fore.MAGENTA}{i}. {task['name']} ({remaining_mins:02d}:{remaining_secs:02d} remaining)")
    
    try:
        task_num = int(input(f"\n{Fore.CYAN}Enter task number to resume: "))
        start_task(task_num)
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid task number!")


def mark_complete(task_num):
    """Mark a task as complete"""
    global tasks
    try:
        if 1 <= task_num <= len(tasks):
            task = tasks[task_num-1]
            task['status'] = f"{Fore.GREEN}Completed ✅"
            
            # Track actual work time for mark complete
            if 'actual_time_worked' not in task:
                task['actual_time_worked'] = 0
            if 'work_sessions' not in task:
                task['work_sessions'] = []
            
            # Add work time based on current progress or full duration if not tracked
            if task['mode'] == 'pomodoro':
                # For Pomodoro tasks, calculate work time from completed Pomodoros
                settings = task['pomodoro_settings']
                completed_pomodoros = len(task.get('pomodoro_history', []))
                total_pomodoros = settings.get('num_pomodoros', 0)
                work_time = completed_pomodoros * settings['work_duration'] * 60
                
                # If task was marked complete before finishing all Pomodoros, add estimated time for remaining work
                if completed_pomodoros < total_pomodoros:
                    remaining_pomodoros = total_pomodoros - completed_pomodoros
                    work_time += remaining_pomodoros * settings['work_duration'] * 60
                
                # Update current_pomodoro to show all pomodoros as completed
                settings['current_pomodoro'] = total_pomodoros
                    
            elif 'remaining' in task:
                # Task was in progress, use worked time
                work_time = task['duration'] - task['remaining']
            else:
                # Task was pending, mark as fully completed
                work_time = task['duration']
            
            task['actual_time_worked'] += work_time
            work_session_data = {
                'duration': work_time,
                'mode': 'marked_complete',
                'timestamp': datetime.now().isoformat()
            }
            
            # Add Pomodoro-specific information if applicable
            if task['mode'] == 'pomodoro':
                work_session_data['pomodoros_completed'] = len(task.get('pomodoro_history', []))
                work_session_data['total_pomodoros'] = task['pomodoro_settings'].get('num_pomodoros', 0)
            
            task['work_sessions'].append(work_session_data)
            
            # Show completion message
            print(f"\n{Fore.GREEN}🎉 Task Completed! 🎉")
            print(f"{Fore.CYAN}Task: {Fore.WHITE}{task['name']}")
            print(f"{Fore.CYAN}Description: {Fore.WHITE}{task['description']}")
            
            # Calculate time saved if completed early
            hrs = task['duration'] // 3600
            mins = (task['duration'] % 3600) // 60
            if task['mode'] == 'custom':
                print(f"{Fore.YELLOW}Originally estimated: {hrs}h {mins}m")
                print(f"{Fore.MAGENTA}Great job completing it early! 💪")
            else:  # pomodoro
                settings = task['pomodoro_settings']
                total = settings.get('num_pomodoros', 0)
                print(f"{Fore.YELLOW}Pomodoro session: {total} total planned")
                print(f"{Fore.MAGENTA}Task completed ahead of schedule! 🚀")
            
            # Optional voice announcement
            speak(f"Task {task['name']} completed!")
            
            print(f"\n{Fore.GREEN}» Task marked as complete! ✅")
            time.sleep(2)
        else:
            print(f"{Fore.RED}Invalid task number!")
            time.sleep(1)
    except (ValueError, IndexError):
        print(f"{Fore.RED}Invalid task number!")
        time.sleep(1)

def pause_screen(task, current_progress, original_duration, mode="normal"):
    """Static pause screen with progress display and completion options"""
    global tasks
    
    while True:
        clear_screen()
        
        # Header based on mode
        if mode == "hyperfocus":
            print(f"\n{Fore.LIGHTMAGENTA_EX}🌟 HYPERFOCUS MODE - PAUSED 🌟\n")
        else:
            print(f"\n{Fore.YELLOW}⏸ TASK PAUSED ⏸\n")
        
        # Task details
        print(f"{Fore.CYAN}Task: {Fore.WHITE}{task['name']}")
        print(f"{Fore.CYAN}Description: {Fore.WHITE}{task['description']}")
        
        # Calculate progress
        progress_percentage = (current_progress / original_duration) * 100
        elapsed_hrs = int(current_progress) // 3600
        elapsed_mins = (int(current_progress) % 3600) // 60
        elapsed_secs = int(current_progress) % 60
        
        remaining = original_duration - current_progress
        remaining_hrs = int(remaining) // 3600
        remaining_mins = (int(remaining) % 3600) // 60
        remaining_secs = int(remaining) % 60
        
        # Progress information
        print(f"\n{Fore.GREEN}📊 Progress Overview:")
        print(f"{Fore.CYAN}Completed: {Fore.WHITE}{elapsed_hrs:02d}h {elapsed_mins:02d}m {elapsed_secs:02d}s")
        print(f"{Fore.CYAN}Remaining: {Fore.WHITE}{remaining_hrs:02d}h {remaining_mins:02d}m {remaining_secs:02d}s")
        print(f"{Fore.CYAN}Progress: {Fore.WHITE}{progress_percentage:.1f}%")
        
        # Visual progress bar
        bar_length = 50
        filled_length = int(bar_length * progress_percentage / 100)
        bar = '▰' * filled_length + '▱' * (bar_length - filled_length)
        print(f"\n{Fore.GREEN}Progress: {progress_percentage:5.1f}%|{bar}| {int(current_progress)}/{int(original_duration)}s")
        
        # Pause duration
        if 'pause_start_time' in task:
            pause_duration = int(time.time() - task['pause_start_time'])
            pause_mins, pause_secs = divmod(pause_duration, 60)
            print(f"{Fore.YELLOW}Paused for: {pause_mins:02d}m {pause_secs:02d}s")
        
        # Options
        print(f"\n{Fore.CYAN}{'─' * 50}")
        print(f"{Fore.GREEN}Options:")
        print(f"{Fore.WHITE}[1] Resume Task")
        print(f"{Fore.WHITE}[2] Mark as Complete")
        print(f"{Fore.WHITE}[3] Go to Main Menu")
        print(f"{Fore.CYAN}{'─' * 50}")
        
        choice = input(f"\n{Fore.MAGENTA}Choose option (1/2/3): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Resume task
            if 'pause_start_time' in task:
                del task['pause_start_time']
            return "resume"
        
        elif choice == "2":
            # Mark as complete
            task['status'] = f"{Fore.GREEN}Completed ✅"
            task['end_time'] = datetime.now().strftime('%H:%M:%S')
            
            # Track actual work time for pause screen completion
            if 'actual_time_worked' not in task:
                task['actual_time_worked'] = 0
            if 'work_sessions' not in task:
                task['work_sessions'] = []
            
            # Add the work time based on current progress
            task['actual_time_worked'] += current_progress
            work_session_data = {
                'duration': current_progress,
                'mode': 'marked_complete_paused',
                'timestamp': datetime.now().isoformat()
            }
            
            # If it's a Pomodoro task, update the current_pomodoro to show completion
            if task['mode'] == 'pomodoro':
                settings = task['pomodoro_settings']
                total_pomodoros = settings.get('num_pomodoros', 0)
                settings['current_pomodoro'] = total_pomodoros
                work_session_data['pomodoros_completed'] = len(task.get('pomodoro_history', []))
                work_session_data['total_pomodoros'] = total_pomodoros
            
            task['work_sessions'].append(work_session_data)
            
            # Show completion message
            print(f"\n{Fore.GREEN}🎉 Task Marked as Complete! 🎉")
            print(f"{Fore.CYAN}Task: {Fore.WHITE}{task['name']}")
            
            # Calculate time saved if completed early
            total_hrs = original_duration // 3600
            total_mins = (original_duration % 3600) // 60
            print(f"{Fore.YELLOW}Originally estimated: {total_hrs}h {total_mins}m")
            print(f"{Fore.MAGENTA}Completed with {remaining_hrs}h {remaining_mins}m remaining! 💪")
            
            # Optional voice announcement
            speak(f"Task {task['name']} completed!")
            
            print(f"\n{Fore.GREEN}» Task marked as complete! ✅")
            time.sleep(3)
            return "completed"
        
        elif choice == "3":
            # Go to main menu
            return "main_menu"
        
        else:
            print(f"{Fore.RED}Invalid choice! Please enter 1, 2, or 3.")
            time.sleep(1)
        

def edit_content(content):
    """Open system editor to modify content"""
    with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False, encoding='utf-8') as tf:
        tf.write(content)
        temp_name = tf.name

    # Open editor based on OS
    if os.name == 'nt':
        os.system(f'notepad.exe "{temp_name}"')
    else:
        editor = os.environ.get('EDITOR', 'vi')
        subprocess.call([editor, temp_name])

    # Read edited content
    with open(temp_name, 'r', encoding='utf-8') as f:
        new_content = f.read().strip()

    os.remove(temp_name)
    return new_content

def format_note_content(note_text):
    """Format note content with colored first line and indented body"""
    lines = note_text.split('\n')
    if not lines:
        return ""
    
    # First line in magenta, rest in white with indentation
    formatted = f"{Fore.MAGENTA}{lines[0]}{Style.RESET_ALL}"
    if len(lines) > 1:
        body = '\n'.join(f"   {line}" for line in lines[1:])
        formatted += f"\n{Fore.WHITE}{body}"
    
    return formatted
    
def notes_interface(backend):
    """Main interface for the notes system with persistence"""
    global notes
    
    while True:
        display_header("NOTES")
        
        # Load notes every time we enter the interface
        saved_data = backend.load_data('notes')
        if saved_data and isinstance(saved_data, dict):
            notes = saved_data.get('modules', {})
        
        if notes:
            print(f"{Fore.BLUE}📒 Note Modules:")
            for i, module in enumerate(notes.keys(), 1):
                note_count = len(notes[module])
                print(f"{Fore.MAGENTA}{i}. {module} ({note_count} notes)")
        else:
            print(f"{Fore.YELLOW}No note modules! Add some first.")
        print()
        
        print(f"{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd Module  [O]pen Module  [D]elete Module  [B]ack")
        cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
        
        if cmd == 'a':
            module_name = input(f"{Fore.CYAN}Enter module name (e.g., Work, Personal): ").strip()
            if module_name:
                if module_name not in notes:
                    notes[module_name] = []
                    save_data = {
                        'modules': notes,
                        'last_modified': datetime.now().strftime('%Y-%m-%d%H:%M:%S.%f')
                    }
                    if backend.save_data(save_data, 'notes'):
                        print(f"{Fore.GREEN}» Module '{module_name}' created! ✅")
                    else:
                        print(f"{Fore.RED}Failed to save module!")
                else:
                    print(f"{Fore.RED}Module already exists!")
        
        elif cmd == 'o':
            if not notes:
                print(f"{Fore.YELLOW}No modules to open!")
                continue
                
            try:
                module_num = int(input(f"{Fore.CYAN}Enter module number: "))
                if 1 <= module_num <= len(notes):
                    module_name = list(notes.keys())[module_num - 1]
                    open_note_module(module_name, backend)
                else:
                    print(f"{Fore.RED}Invalid module number!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        elif cmd == 'd':
            if not notes:
                print(f"{Fore.YELLOW}No modules to delete!")
                continue
                
            try:
                module_num = int(input(f"{Fore.CYAN}Enter module number to delete: "))
                if 1 <= module_num <= len(notes):
                    module_name = list(notes.keys())[module_num - 1]
                    confirm = input(f"{Fore.YELLOW}Are you sure you want to delete '{module_name}'? (y/n): ").lower()
                    if confirm == 'y':
                        del notes[module_name]
                        save_data = {
                            'modules': notes,
                            'last_modified': datetime.now().strftime('%Y-%m-%d%H:%M:%S.%f')
                        }
                        if backend.save_data(save_data, 'notes'):
                            print(f"{Fore.GREEN}Module deleted successfully!")
                        else:
                            print(f"{Fore.RED}Failed to delete module!")
                else:
                    print(f"{Fore.RED}Invalid module number!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        elif cmd == 'b':
            break

def open_note_in_notepad(initial_content="", instructions=""):
    """Open notepad for editing and return the content"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as tf:
            # Add clear instructions at the top
            tf.write("""TASKMAN Note Instructions:
1. Delete these instruction lines (including the dashed line below)
2. Write your note below
3. Press Ctrl+S to save
4. Close Notepad to view changes in TASKMAN
----------------------------------------

""")
            # Add any existing content
            if initial_content:
                tf.write(initial_content)
            temp_path = tf.name

        # Open notepad with the temp file
        if os.name == 'nt':  # Windows
            subprocess.run(['notepad.exe', temp_path], check=True)
        else:  # Unix-like systems
            subprocess.run(['nano', temp_path], check=True)

        # Read the content back
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove instructions if they were added
        if "TASKMAN Note Instructions:" in content:
            content = content.split("----------------------------------------\n\n", 1)[-1]

        # Clean up
        os.unlink(temp_path)
        return content.strip()

    except Exception as e:
        print(f"{Fore.RED}Error using notepad: {str(e)}")
        return None

def open_note_module(module_name, backend):
    """Interface for managing notes within a module"""
    global notes
    
    if module_name not in notes:
        notes[module_name] = []
        backend.save_data({'modules': notes}, 'notes')
    
    while True:
        display_header(f"NOTES - {module_name}")
        
        notes_data = backend.load_data('notes')
        if notes_data and 'modules' in notes_data:
            notes = notes_data['modules']
        
        if notes[module_name]:
            print(f"{Fore.BLUE}📝 Notes in {module_name}:")
            for i, note in enumerate(notes[module_name], 1):
                if isinstance(note, dict):
                    content = note['content']
                    timestamp = note.get('last_modified', 'Unknown date')
                else:
                    content = note
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    notes[module_name][i-1] = {
                        'content': content,
                        'last_modified': timestamp
                    }
                    backend.save_data({'modules': notes}, 'notes')
                
                print(f"{Fore.CYAN}{i}. {format_note_content(content)}")
                print(f"   {Fore.YELLOW}Last modified: {timestamp}")
                print(f"   {Fore.BLUE}{'─' * 40}")
        else:
            print(f"{Fore.YELLOW}No notes in this module!")
        
        print(f"\n{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd Note  [E]dit Note  [D]elete Note  [B]ack")
        cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
        
        if cmd == 'a':
            content = open_note_in_notepad()
            if content:
                note_data = {
                    'content': content,
                    'last_modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                notes[module_name].append(note_data)
                if backend.save_data({'modules': notes}, 'notes'):
                    print(f"{Fore.GREEN}Note added successfully!")
                    notes_data = backend.load_data('notes')
                    if notes_data and 'modules' in notes_data:
                        notes = notes_data['modules']
                else:
                    print(f"{Fore.RED}Failed to save note!")
            time.sleep(1)
        
        elif cmd == 'e':
            if not notes[module_name]:
                print(f"{Fore.RED}No notes to edit!")
                continue
            
            try:
                note_num = int(input(f"{Fore.CYAN}Enter note number to edit: ")) - 1
                if 0 <= note_num < len(notes[module_name]):
                    current_note = notes[module_name][note_num]
                    content = current_note['content'] if isinstance(current_note, dict) else current_note
                    edited_content = open_note_in_notepad(initial_content=content)
                    if edited_content:
                        note_data = {
                            'content': edited_content,
                            'last_modified': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        notes[module_name][note_num] = note_data
                        if backend.save_data({'modules': notes}, 'notes'):
                            print(f"{Fore.GREEN}Note edited successfully!")
                        else:
                            print(f"{Fore.RED}Failed to edit note!")
                else:
                    print(f"{Fore.RED}Invalid note number!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        elif cmd == 'd':
            if not notes[module_name]:
                print(f"{Fore.RED}No notes to delete!")
                continue
            
            try:
                note_num = int(input(f"{Fore.CYAN}Enter note number to delete: ")) - 1
                if 0 <= note_num < len(notes[module_name]):
                    confirm = input(f"{Fore.YELLOW}Are you sure you want to delete this note? (y/n): ").lower()
                    if confirm == 'y':
                        notes[module_name].pop(note_num)
                        if backend.save_data({'modules': notes}, 'notes'):
                            print(f"{Fore.GREEN}Note deleted successfully!")
                        else:
                            print(f"{Fore.RED}Failed to delete note!")
                else:
                    print(f"{Fore.RED}Invalid note number!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        elif cmd == 'b':
            break
        
        time.sleep(1)

def fast_notes_interface(backend):
    """Interface for quick notes management"""
    global quick_notes
    
    while True:
        display_header("FAST NOTES")
        
        # Reload fast notes data to ensure we have latest
        fastnotes_data = backend.load_data('fastnotes')
        if fastnotes_data:
            quick_notes = fastnotes_data
        
        if quick_notes:
            print(f"{Fore.BLUE}📝 Quick Notes:")
            for i, note in enumerate(quick_notes, 1):
                if isinstance(note, dict):
                    content = note['content']
                    timestamp = note.get('timestamp', 'Unknown date')
                else:
                    content = note
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    quick_notes[i-1] = {
                        'content': content,
                        'timestamp': timestamp
                    }
                    backend.save_data(quick_notes, 'fastnotes')
                
                print(f"{Fore.CYAN}{i}. {format_note_content(content)}")
                print(f"   {Fore.YELLOW}Created: {timestamp}")
                print(f"   {Fore.BLUE}{'─' * 40}")
        else:
            print(f"{Fore.YELLOW}No quick notes yet!")
        
        print(f"\n{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd Note  [E]dit Note  [D]elete Note  [B]ack")
        cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
        
        if cmd == 'a':
            content = open_note_in_notepad()
            if content:
                new_note = {
                    'content': content,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                quick_notes.append(new_note)
                if backend.save_data(quick_notes, 'fastnotes'):
                    print(f"{Fore.GREEN}Quick note added successfully!")
                else:
                    print(f"{Fore.RED}Failed to save quick note!")
            time.sleep(1)
        
        elif cmd == 'e':
            if not quick_notes:
                print(f"{Fore.RED}No quick notes to edit!")
                continue
            
            try:
                note_num = int(input(f"{Fore.CYAN}Enter note number to edit: ")) - 1
                if 0 <= note_num < len(quick_notes):
                    current_note = quick_notes[note_num]
                    content = current_note['content'] if isinstance(current_note, dict) else current_note
                    edited_content = open_note_in_notepad(initial_content=content)
                    if edited_content:
                        quick_notes[note_num] = {
                            'content': edited_content,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        if backend.save_data(quick_notes, 'fastnotes'):
                            print(f"{Fore.GREEN}Quick note edited successfully!")
                        else:
                            print(f"{Fore.RED}Failed to edit quick note!")
                else:
                    print(f"{Fore.RED}Invalid note number!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        elif cmd == 'd':
            if not quick_notes:
                print(f"{Fore.RED}No quick notes to delete!")
                continue
            
            try:
                note_num = int(input(f"{Fore.CYAN}Enter note number to delete: ")) - 1
                if 0 <= note_num < len(quick_notes):
                    confirm = input(f"{Fore.YELLOW}Are you sure you want to delete this note? (y/n): ").lower()
                    if confirm == 'y':
                        quick_notes.pop(note_num)
                        if backend.save_data(quick_notes, 'fastnotes'):
                            print(f"{Fore.GREEN}Quick note deleted successfully!")
                        else:
                            print(f"{Fore.RED}Failed to delete quick note!")
                else:
                    print(f"{Fore.RED}Invalid note number!")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number!")
        
        elif cmd == 'b':
            break
        
        time.sleep(1)

def generate_daily_report(date_str=None):
    """Generate a detailed daily report with charts and statistics"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Load tasks for the specified date
    historical_data = backend.load_tasks(date_str)
    if not historical_data:
        print(f"{Fore.YELLOW}No tasks found for {date_str}")
        return None

    tasks_list = historical_data.get('tasks', [])
    if not tasks_list:
        print(f"{Fore.YELLOW}No tasks found for {date_str}")
        return None

    # Calculate statistics
    total_time = 0
    completed_time = 0
    longest_session = 0
    longest_task_name = ""
    completed_tasks = 0
    pending_tasks = 0
    paused_tasks = 0

    task_details = []
    
    for task in tasks_list:
        duration = task['duration']
        status = task['status'].replace(Fore.GREEN, '').replace(Fore.YELLOW, '').replace(Fore.BLUE, '')
        
        task_details.append({
            'name': task['name'],
            'duration': duration,
            'status': status,
            'description': task['description']
        })

        total_time += duration
        
        if "Completed" in status:
            completed_time += duration
            completed_tasks += 1
            # Check if this was the longest session
            if duration > longest_session:
                longest_session = duration
                longest_task_name = task['name']
        elif "Paused" in status:
            paused_tasks += 1
        else:
            pending_tasks += 1

    # Generate report content
    report = [
        f"📊 TASKMAN DAILY REPORT - {date_str} 📊",
        "=" * 50,
        "\n📈 SUMMARY STATISTICS",
        "-" * 20,
        f"Total Time Allocated: {total_time//3600}h {(total_time%3600)//60}m",
        f"Time Spent on Completed Tasks: {completed_time//3600}h {(completed_time%3600)//60}m",
        f"Longest Single Session: {longest_session//3600}h {(longest_session%3600)//60}m ({longest_task_name})",
        f"Completion Rate: {(completed_tasks/len(tasks_list))*100:.1f}%",
        f"\nTask Status Distribution:",
        f"✅ Completed: {completed_tasks}",
        f"⏸ Paused: {paused_tasks}",
        f"⏳ Pending: {pending_tasks}",
        "\n📋 DETAILED TASK BREAKDOWN",
        "-" * 20
    ]

    # Add individual task details
    for idx, task in enumerate(task_details, 1):
        duration = task['duration']
        report.extend([
            f"\nTask {idx}: {task['name']}",
            f"Description: {task['description']}",
            f"Duration: {duration//3600}h {(duration%3600)//60}m",
            f"Status: {task['status']}"
        ])

    return report

def display_report(report):
    """Display the report with colored formatting"""
    clear_screen()
    
    # Print header
    print(f"\n{Fore.CYAN}{report[0]}")
    print(f"{Fore.CYAN}{report[1]}\n")
    
    # Print statistics section
    print(f"{Fore.GREEN}{report[2]}")
    print(f"{Fore.GREEN}{report[3]}")
    
    # Print summary stats with colors
    for line in report[4:8]:
        print(f"{Fore.YELLOW}{line}")
    
    # Print status distribution
    print(f"\n{Fore.YELLOW}{report[8]}")
    print(f"{Fore.GREEN}{report[9]}")  # Completed
    print(f"{Fore.YELLOW}{report[10]}")  # Paused
    print(f"{Fore.RED}{report[11]}")  # Pending
    
    # Print detailed breakdown
    print(f"\n{Fore.GREEN}{report[12]}")
    print(f"{Fore.GREEN}{report[13]}")
    
    # Print task details
    for i in range(14, len(report)):
        if report[i].startswith('\nTask'):
            print(f"\n{Fore.CYAN}{report[i]}")
        else:
            print(f"{Fore.WHITE}{report[i]}")

def export_report(report, date_str=None):
    """Export the report to a text file"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(backend.data_dir, "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    filename = os.path.join(reports_dir, f"taskman_report_{date_str}.txt")
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for line in report:
                f.write(line + '\n')
        return filename
    except Exception as e:
        print(f"{Fore.RED}Error exporting report: {str(e)}")
        return None

def report_interface():
    """Interface for viewing and exporting reports"""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}📊 TASKMAN REPORTS 📊\n")
        print(f"{Fore.YELLOW}1. View Today's Report")
        print(f"{Fore.YELLOW}2. View Report for Specific Date")
        print(f"{Fore.YELLOW}3. Export Report")
        print(f"{Fore.YELLOW}4. Back to Main Menu")
        
        choice = input(f"\n{Fore.GREEN}Choice (1-4): ").strip()
        
        if choice == '1':
            report = generate_daily_report()
            if report:
                display_report(report)
                input(f"\n{Fore.CYAN}Press Enter to continue...")
        
        elif choice == '2':
            date_str = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                report = generate_daily_report(date_str)
                if report:
                    display_report(report)
                    input(f"\n{Fore.CYAN}Press Enter to continue...")
            except ValueError:
                print(f"{Fore.RED}Invalid date format!")
                time.sleep(1)
        
        elif choice == '3':
            date_str = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                report = generate_daily_report(date_str)
                if report:
                    filename = export_report(report, date_str)
                    if filename:
                        print(f"{Fore.GREEN}Report exported to: {filename}")
                        time.sleep(2)
            except ValueError:
                print(f"{Fore.RED}Invalid date format!")
                time.sleep(1)
        
        elif choice == '4':
            break
        
        else:
            print(f"{Fore.RED}Invalid choice!")
            time.sleep(1)

def view_task_details(task):
    """Display details for a single task"""
    clear_screen()
    print(f"\n{Fore.CYAN}Task Details:\n")
    print(f"{Fore.CYAN}Task: {Fore.GREEN}{task['name']}")
    print(f"{Fore.CYAN}Description: {Fore.WHITE}{task['description']}")
    print(f"{Fore.CYAN}Status: {task['status']}")
    
    # Show start and end times only if they exist
    start_time = task.get('start_time', 'Not started')
    end_time = task.get('end_time', 'N/A')
    
    if start_time != 'Not started':
        print(f"{Fore.CYAN}Started at: {Fore.WHITE}{start_time}")
    if end_time != 'N/A' and "Completed" in task['status']:
        print(f"{Fore.CYAN}Ended at: {Fore.WHITE}{end_time}")
    
    if task['mode'] == 'pomodoro':
        settings = task['pomodoro_settings']
        total = settings.get('num_pomodoros', 0)
        
        # Check if task is completed - if so, show all pomodoros as completed
        if "Completed" in task['status']:
            completed = total
        else:
            # For active tasks, use current_pomodoro or pomodoro_history length
            completed = max(
                settings.get('current_pomodoro', 0),
                len(task.get('pomodoro_history', []))
            )
        
        print(f"\n{Fore.YELLOW}Pomodoro Details:")
        print(f"Progress: {completed}/{total} Pomodoros")
        print(f"Work Duration: {settings['work_duration']} minutes")
        print(f"Break Duration: {settings['break_duration']} minutes")
        print(f"Long Break Duration: {settings['long_break_duration']} minutes")
        
        if task.get('pomodoro_history'):
            print(f"\n{Fore.YELLOW}Session History:")
            for i, pomo in enumerate(task['pomodoro_history'], 1):
                print(f"  #{i}: {pomo['timestamp']} - Work: {pomo['work_duration']}min")
    else:
        hrs = task['duration'] // 3600
        mins = (task['duration'] % 3600) // 60
        print(f"\n{Fore.YELLOW}Duration: {hrs}h {mins}m")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...")

def view_tasks():
    """Interface for viewing task details"""
    while True:
        clear_screen()
        print(f"\n{Fore.CYAN}📋 TASK DETAILS 📋\n")
        
        # Display all tasks with numbers
        for i, task in enumerate(tasks, 1):
            # Changed the format to put number inside brackets
            if task['mode'] == 'custom':
                print(f"{Fore.RED}[{i}] {task['name']} - {task['status']}")
            else:
                print(f"{Fore.MAGENTA}[{i}] 🍅 {task['name']} - {task['status']}")
        
        print(f"\n{Fore.YELLOW}Enter task number to view details (or 'b' to go back)")
        choice = input(f"{Fore.GREEN}Choice: ").strip().lower()
        
        if choice == 'b':
            break
        
        try:
            task_num = int(choice)
            if 1 <= task_num <= len(tasks):
                view_task_details(tasks[task_num-1])
            else:
                print(f"{Fore.RED}Invalid task number!")
                time.sleep(1)
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number!")
            time.sleep(1)

def help_menu():
    """Display help menu with detailed information"""
    while True:
        display_header("HELP MENU")
        help_text = f"""
{Fore.GREEN}📚 TASKMAN Help Guide

{Fore.CYAN}1. Task Management
{Fore.YELLOW}2. Focus Modes
{Fore.MAGENTA}3. Reports & Statistics
{Fore.BLUE}4. Notes System
{Fore.WHITE}5. Keyboard Shortcuts
{Fore.LIGHTGREEN_EX}6. Feedbacks & Suggestions
{Fore.RED}7. Back to Main Menu

Choose a topic (1-7): """
        
        choice = input(help_text).strip()
        
        if choice == '1':
            clear_screen()
            print(f"""
{Fore.GREEN}📌 Task Management

{Fore.CYAN}Creating Tasks:
{Fore.WHITE}• Choose between Custom or Pomodoro tasks
• Set duration, description, and other parameters
• Use 'A' command to add new tasks

{Fore.CYAN}Managing Tasks:
{Fore.WHITE}• Start tasks with 'S' or 'SX' (X = task number)
• Pause/Resume with 'P' command
• Edit tasks with 'E' or 'EX'
• Delete tasks with 'D' or 'DX'
• Mark complete with 'M' or 'MX' (skip timer)
• View task details with 'V' or 'VX'

{Fore.CYAN}Task Status:
{Fore.WHITE}• Pending - Not started
• In Progress - Currently running
• Paused - Temporarily stopped
• Completed - Finished successfully
""")
        elif choice == '2':
            clear_screen()
            print(f"""
{Fore.YELLOW}🎯 Focus Modes

{Fore.CYAN}Normal Mode:
{Fore.WHITE}• Standard progress tracking
• Full interface visibility
• Access to all commands

{Fore.CYAN}HyperFocus Mode:
{Fore.WHITE}• Distraction-free environment
• Enhanced visual feedback
• Minimalist interface
• Quick access to notes

{Fore.CYAN}Pomodoro Mode:
{Fore.WHITE}• Structured work/break intervals
• Customizable durations
• Session tracking
• Break notifications
""")
        elif choice == '3':
            clear_screen()
            print(f"""
{Fore.MAGENTA}📊 Reports & Statistics

{Fore.CYAN}Daily Reports:
{Fore.WHITE}• View today's progress
• Task completion rates
• Time allocation analysis
• Session statistics

{Fore.CYAN}Historical Data:
{Fore.WHITE}• Access past tasks with 'H' command
• View reports for specific dates
• Track productivity trends

{Fore.CYAN}Export Options:
{Fore.WHITE}• Save reports as text files
• Detailed session breakdowns
• Time-stamped entries
""")
        elif choice == '4':
            clear_screen()
            print(f"""
{Fore.BLUE}📝 Notes System

{Fore.CYAN}Modular Notes:
{Fore.WHITE}• Organize notes in modules
• Create custom categories
• Full text editor support
• Access with 'N' command

{Fore.CYAN}Fast Notes:
{Fore.WHITE}• Quick capture system
• Instant note creation
• Access with 'F' command
• Perfect for quick thoughts

{Fore.CYAN}Note Management:
{Fore.WHITE}• Edit existing notes
• Delete unwanted notes
• Move between modules
• Search functionality
""")
        elif choice == '5':
            clear_screen()
            print(f"""
{Fore.WHITE}⌨️ Keyboard Shortcuts

{Fore.CYAN}Main Commands:
{Fore.WHITE}• A - Add new task
• L - List all tasks
• S/SX - Start task
• P - Pause/Resume task
• E/EX - Edit task
• D/DX - Delete task
• M/MX - Mark task complete
• V/VX - View task details
• N - Open notes
• F - Open fast notes
• H - View history
• R - Open reports
• Q - Quit application
• ? - Open this help menu

{Fore.CYAN}During Task:
{Fore.WHITE}• Ctrl+C - Interrupt task
• P - Pause task
• H - Switch to HyperFocus
• N - Quick access to notes
• F - Quick access to fast notes
""")
        elif choice == '6':
            clear_screen()
            print(f"""
{Fore.LIGHTGREEN_EX}📝 Feedbacks & Suggestions

{Fore.CYAN}We'd love to hear from you!
{Fore.WHITE}• Share your thoughts, suggestions, or report issues
• Your feedback helps us improve TASKMAN
• We appreciate your input and support

{Fore.CYAN}Contact us:
{Fore.YELLOW}📧 Write to us at: {Fore.WHITE}thehardclub.contact@gmail.com

{Fore.GREEN}Thank you for being part of The Hard Club community! 🙏
""")
        elif choice == '7':
            break
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

def cloud_integration_interface():
    """Cloud Integration and The Hard Club Suite Information"""
    while True:
        display_header("CLOUD INTEGRATION")
        
        print(f"""
{Fore.LIGHTBLUE_EX}🌐 Welcome to TaskMan-SV Cloud Integration

{Fore.GREEN}📦 About The Hard Club Suite:
{Fore.WHITE}TaskMan-SV is proudly part of {Fore.CYAN}The Hard Club{Fore.WHITE} - a comprehensive suite of 
productivity tools designed to enhance your workflow and maximize efficiency.

{Fore.YELLOW}🔧 Current Version - Offline & Free:
{Fore.WHITE}• ✅ Fully offline task management
• ✅ Secure local data storage
• ✅ Cross-platform compatibility
• ✅ Zero subscription fees
• ✅ Complete privacy control

{Fore.LIGHTMAGENTA_EX}☁️ Future Cloud Integration Benefits:
{Fore.WHITE}• 🔄 Sync tasks across all your devices
• 📱 Mobile app integration
• 🌐 Web dashboard access
• 👥 Team collaboration features
• 📊 Advanced analytics & insights
• 🔒 Encrypted cloud storage
• ⚡ Real-time synchronization

{Fore.CYAN}🚀 Ready to Go Cloud?
{Fore.WHITE}If you're interested in taking your productivity to the next level with 
cloud synchronization and mobile access, we'd love to hear from you!

{Fore.GREEN}📧 Contact Information:
{Fore.WHITE}Email: {Fore.LIGHTCYAN_EX}thehardclub.contact@gmail.com{Fore.WHITE}
Website: {Fore.LIGHTCYAN_EX}www.thehardclub.com{Fore.WHITE}

{Fore.YELLOW}📝 What to Include in Your Email:
{Fore.WHITE}• Your current TaskMan-SV usage
• Devices you'd like to sync
• Specific features you're interested in
• Any questions about cloud integration

{Fore.LIGHTGREEN_EX}💡 Pro Tip: {Fore.YELLOW}Mention "TaskMan-SV Cloud Interest" in your subject line 
for priority response!{Style.RESET_ALL}
        """)
        
        print(f"\n{Fore.CYAN}{'─' * 70}")
        print(f"{Fore.GREEN}Options:")
        print(f"{Fore.WHITE}[1] Copy Email Address")
        print(f"{Fore.WHITE}[2] Visit Website Info")
        print(f"{Fore.WHITE}[3] Back to Main Menu")
        print(f"{Fore.CYAN}{'─' * 70}")
        
        choice = input(f"\n{Fore.MAGENTA}Choose option (1/2/3): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            # Display email for easy copying
            print(f"\n{Fore.GREEN}📋 Email Address for Copy:")
            print(f"{Fore.LIGHTCYAN_EX}thehardclub.contact@gmail.com{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}💡 Tip: Select the email above and copy it (Ctrl+C)")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        elif choice == "2":
            # Display website info
            print(f"\n{Fore.GREEN}🌐 Website Information:")
            print(f"{Fore.LIGHTCYAN_EX}www.thehardclub.com{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Visit our website to explore:")
            print(f"{Fore.WHITE}• Other productivity tools in our suite")
            print(f"{Fore.WHITE}• Latest updates and announcements")
            print(f"{Fore.WHITE}• Community and support resources")
            print(f"{Fore.WHITE}• Blog posts on productivity tips")
            input(f"\n{Fore.CYAN}Press Enter to continue...")
            
        elif choice == "3":
            break
            
        else:
            print(f"{Fore.RED}Invalid choice! Please enter 1, 2, or 3.")
            time.sleep(1)

def load_saved_data():
    """Load all saved data from backend"""
    global notes, quick_notes, tasks
    
    # Load notes
    saved_notes = backend.load_data('notes')
    if isinstance(saved_notes, dict) and 'modules' in saved_notes:
        notes.update(saved_notes['modules'])
    
    # Load quick notes
    saved_fastnotes = backend.load_data('fastnotes')
    if isinstance(saved_fastnotes, list):
        quick_notes.extend(saved_fastnotes)
    
    # Load tasks
    saved_tasks = backend.load_data('tasks')
    if isinstance(saved_tasks, list):
        tasks.extend(saved_tasks)

def main_interface():
    """Main interface with flexible command input handling"""
    global backend, tasks, notes, quick_notes
    session_count = 0
    last_auto_save = datetime.now().date()
    
    try:
        # Show welcome banner first, before authentication
        welcome_banner()
        
        backend = setup_backend()
        if not backend:
            print(f"{Fore.RED}Authentication failed!")
            return

        # Load existing data
        today = date.today().isoformat()
        task_data = backend.load_tasks(today)
        if task_data:
            tasks = task_data["tasks"]

        notes_data = backend.load_data('notes')
        if notes_data and 'modules' in notes_data:
            notes = notes_data['modules']
        else:
            notes = {}

        fastnotes_data = backend.load_data('fastnotes')
        if fastnotes_data:
            quick_notes = fastnotes_data
        else:
            quick_notes = []

        # Remove the duplicate welcome_banner() call that was here
        
        while True:
            # Check if we need to auto-save the report
            current_date = datetime.now().date()
            
            # Auto-save report if date changed
            if current_date != last_auto_save:
                report = generate_daily_report(last_auto_save.isoformat())
                if report:
                    backend.save_report(report, last_auto_save.isoformat())
                last_auto_save = current_date
                session_count = 0
            
            # Auto-save report after every 5 sessions
            if session_count >= 5:
                report = generate_daily_report()
                if report:
                    backend.save_report(report)
                session_count = 0
            
            display_header()
            display_tasks()
            
            print(f"{Fore.CYAN}Commands: {Fore.YELLOW}[A]dd  [S]tartX  [P]auseX/Resume  [E]ditX  [D]eleteX  [M]arkCompleteX  [V]iewX  [N]otes  [F]astNotes  [C]loud  [H]istory  [R]eports  [?]Help/Contact  [Q]uit")
            
            try:
                cmd = input(f"{Fore.MAGENTA}» ").strip().lower()
                
                # Handle view command with optional task number
                if cmd.startswith('v'):
                    task_num = None
                    # Check if command includes a task number (e.g., "v2")
                    if len(cmd) > 1 and cmd[1:].isdigit():
                        task_num = int(cmd[1:])
                        if 1 <= task_num <= len(tasks):
                            view_task_details(tasks[task_num-1])
                            continue
                        else:
                            print(f"{Fore.RED}Invalid task number!")
                            time.sleep(1)
                            continue
                    view_tasks()
                    backend.save_tasks(tasks)
                
                elif cmd == 'a':
                    add_task()
                    backend.save_tasks(tasks)
                
                elif cmd.startswith('s'):
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    start_task(num)
                    backend.save_tasks(tasks)
                
                elif cmd.startswith('d'):
                    if len(tasks) == 0:
                        print(f"{Fore.RED}No tasks to delete!")
                        time.sleep(1)
                        continue
                    
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number to delete: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    
                    # Validate task number and delete
                    if 1 <= num <= len(tasks):
                        deleted_task = tasks.pop(num - 1)
                        print(f"{Fore.GREEN}✅ Task '{deleted_task['name']}' deleted successfully!")
                    else:
                        print(f"{Fore.RED}Invalid task number!")
                        time.sleep(1)
                    backend.save_tasks(tasks)
                
                elif cmd.startswith('e'):
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number to edit: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    edit_task(num)
                
                elif cmd.startswith('m'):
                    try:
                        # Try to get number from command
                        num = int(cmd[1:])
                    except ValueError:
                        # If no number in command, ask for it
                        try:
                            num = int(input(f"{Fore.CYAN}Enter task number to mark complete: "))
                        except ValueError:
                            print(f"{Fore.YELLOW}Please enter a valid task number.")
                            time.sleep(1)
                            continue
                    mark_complete(num)
                    backend.save_tasks(tasks)
                
                elif cmd == 'p':
                    resume_task()
                    backend.save_tasks(tasks)
                
                elif cmd == 'n':
                    notes_interface(backend)
                
                elif cmd == 'f':
                    fast_notes_interface(backend)
                
                elif cmd == 'c':
                    cloud_integration_interface()
                
                elif cmd == 'h':
                    # New history viewing feature
                    date_input = input(f"{Fore.CYAN}Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                    if not date_input:
                        date_input = today
                    try:
                        # Validate date format
                        datetime.strptime(date_input, '%Y-%m-%d')
                        historical_data = backend.load_tasks(date_input)
                        if historical_data:
                            print(f"\n{Fore.GREEN}Tasks for {date_input}:")
                            for i, task in enumerate(historical_data['tasks'], 1):
                                hrs = task['duration'] // 3600
                                mins = (task['duration'] % 3600) // 60
                                print(f"{Fore.MAGENTA}{i}. {task['name']} [{hrs}h {mins}m] - {task['status']}")
                        else:
                            print(f"{Fore.YELLOW}No tasks found for {date_input}")
                        input(f"\n{Fore.CYAN}Press Enter to continue...")
                    except ValueError:
                        print(f"{Fore.RED}Invalid date format! Use YYYY-MM-DD")
                        time.sleep(1)
                
                elif cmd == 'r':
                    report_interface()
                
                elif cmd == '?':
                    help_menu()
                
                elif cmd == 'q':
                    # Save final state before quitting
                    backend.save_tasks(tasks)
                    clear_screen()
                    print(f"\n{Fore.BLUE}🚪 Goodbye! Keep being awesome! 💪\n")
                    break
                
                else:
                    print(f"{Fore.YELLOW}Unknown command. See options above")
                    time.sleep(1)
                    
                # Update session count when a task is completed
                if cmd.startswith('s'):
                    session_count += 1

            except KeyboardInterrupt:
                # Save final report before exiting
                report = generate_daily_report()
                if report:
                    backend.save_report(report)
                backend.save_tasks(tasks)
                clear_screen()
                print(f"\n{Fore.BLUE}🚪 Goodbye! Keep being awesome! 💪\n")
                break
            
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {str(e)}")
                time.sleep(1)
                continue

    except Exception as e:
        print(f"{Fore.RED}Critical error: {str(e)}")
        print(f"{Fore.YELLOW}Please try restarting TASKMAN")

if __name__ == "__main__":
    main_interface()