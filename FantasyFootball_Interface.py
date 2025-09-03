import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
import subprocess
import platform
import threading
import time

# Helper function for resource paths 
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Sample player video mappings
'''PLAYER_VIDEOS = {
    "Ja'Marr Chase": "videos/JaMarr_Chase.mp4",
    "Bijan Robinson": "videos/Bijan_Robinson.mp4",
    "CeeDee Lamb": "videos/CeeDee_Lamb.mp4",
    "Saquon Barkley": "videos/Saquon_Barkley.mp4",
    "Justin Jefferson": "videos/Justin_Jefferson.mp4",
    "Jahmyr Gibbs": "videos/Jahmyr_Gibbs.mp4",
    "Malik Nabers": "videos/Malik_Nabers.mp4",
    "Christian McCaffrey": "videos/Christian_McCaffrey.mp4",
    "Nico Collins": "videos/Nico_Collins.mp4",
    "Puka Nacua": "videos/Puka_Nacua.mp4",
    "Ashton Jeanty": "videos/Ashton_Jeanty.mp4",
    "Brian Thomas": "videos/Brian_Thomas.mp4",
    "Derrick Henry": "videos/Derrick_Henry.mp4",
    "Amon-Ra St. Brown": "videos/Amon_Ra_St_Brown.mp4",
    "De'Von Achane": "videos/DeVon_Achane.mp4",
    "Brock Bowers": "videos/Brock_Bowers.mp4",
    "A.J. Brown": "videos/AJ_Brown.mp4",
    "Drake London": "videos/Drake_London.mp4",
    "Bucky Irving": "videos/Bucky_Irving.mp4",
    "Chase Brown": "videos/Chase_Brown.mp4",
    "Josh Jacobs": "videos/Josh_Jacobs.mp4",
    "Jonathan Taylor": "videos/Jonathan_Taylor.mp4",
    "Trey McBride": "videos/Trey_McBride.mp4",
    "Ladd McConkey": "videos/Ladd_McConkey.mp4",
    "Josh Allen": "videos/Josh_Allen.mp4",
    "Lamar Jackson": "videos/Lamar_Jackson.mp4",
    "Kyren Williams": "videos/Kyren_Williams.mp4",
    "Tee Higgins": "videos/Tee_Higgins.mp4",
    "Jayden Daniels": "videos/Jayden_Daniels.mp4",
    "Jaxon Smith-Njigba": "videos/Jaxon_Smith_Njigba.mp4",
    "Tyreek Hill": "videos/Tyreek_Hill.mp4",
    "Jalen Hurts": "videos/Jalen_Hurts.mp4",
    "Mike Evans": "videos/Mike_Evans.mp4",
    "George Kittle": "videos/George_Kittle.mp4",
    "James Cook": "videos/James_Cook.mp4",
    "Davante Adams": "videos/Davante_Adams.mp4",
    "Omarion Hampton": "videos/Omarion_Hampton.mp4",
    "Kenneth Walker": "videos/Kenneth_Walker.mp4",
    "Garrett Wilson": "videos/Garrett_Wilson.mp4",
    "Marvin Harrison": "videos/Marvin_Harrison.mp4",
    "Tetairoa McMillan": "videos/Tetairoa_McMillan.mp4",
    "Terry McLaurin": "videos/Terry_McLaurin.mp4",
    "Xavier Worthy": "videos/Xavier_Worthy.mp4",
    "TreVeyon Henderson": "videos/TreVeyon_Henderson.mp4",
    "Alvin Kamara": "videos/Alvin_Kamara.mp4",
    "DK Metcalf": "videos/DK_Metcalf.mp4",
    "Chuba Hubbard": "videos/Chuba_Hubbard.mp4",
    "DJ Moore": "videos/DJ_Moore.mp4",
    "Breece Hall": "videos/Breece_Hall.mp4",
    "DeVonta Smith": "videos/DeVonta_Smith.mp4"
}
'''
from PLAYER_VIDEOS import PLAYER_VIDEOS


class AnimatedButton(tk.Button):
    """Enhanced button with hover animations and gradient-like effects"""
    
    def __init__(self, parent, **kwargs):
        self.normal_bg = kwargs.pop('normal_bg', '#3b82f6')
        self.hover_bg = kwargs.pop('hover_bg', '#2563eb')
        self.active_bg = kwargs.pop('active_bg', '#1d4ed8')
        
        # Default styling with dark text for readability
        default_style = {
            'bg': self.normal_bg,
            'fg': 'black', 
            'relief': 'flat',
            'font': ('Segoe UI', 10, 'bold'),
            'cursor': 'hand2',
            'bd': 0,
            'padx': 20,
            'pady': 8
        }
        
        for key, value in default_style.items():
            if key not in kwargs:
                kwargs[key] = value
                
        super().__init__(parent, **kwargs)
        
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def on_hover(self, event):
        self.config(bg=self.hover_bg)
    
    def on_leave(self, event):
        self.config(bg=self.normal_bg)
    
    def on_click(self, event):
        self.config(bg=self.active_bg)
    
    def on_release(self, event):
        self.config(bg=self.hover_bg)

class GradientFrame(tk.Frame):
    """Frame with gradient-like background using multiple colors"""
    
    def __init__(self, parent, color1='#1e293b', color2='#0f172a', **kwargs):
        super().__init__(parent, bg=color1, **kwargs)
        self.color1 = color1
        self.color2 = color2

class ModernEntry(tk.Entry):
    """Styled entry with modern appearance"""
    
    def __init__(self, parent, **kwargs):
        default_style = {
            'bg': '#374151',
            'fg': '#f9fafb',
            'insertbackground': '#f9fafb',
            'relief': 'flat',
            'bd': 0,
            'font': ('Segoe UI', 11),
            'highlightthickness': 2,
            'highlightcolor': '#3b82f6',
            'highlightbackground': '#6b7280'
        }
        
        for key, value in default_style.items():
            if key not in kwargs:
                kwargs[key] = value
                
        super().__init__(parent, **kwargs)
        
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
    
    def on_focus_in(self, event):
        self.config(bg='#4b5563')
    
    def on_focus_out(self, event):
        self.config(bg='#374151')

class FantasyDraftApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Fantasy Football Draft Picker")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        self.root.configure(bg="#0f172a")
        
        # Constants
        self.ROUNDS = 15
        self.STAT_COLUMNS = [
            "Player", "Total Points (Prev Year)", "Projected Points", "Rush Yards", 
            "Receiving Yards", "Passing Yards", "Pass TD", "Rush Att", "Rush TD", "Receptions", 
            "Rec TD", "2-PT", "Fumble Lost", "Targets", "Fumble Return TD",'Team', 'Position',
            'Target Share', 'Fantasy PPG', 'Games', 'Bye Week', 'Matchups', 'ADP', 'WR ADP'
            ]

        
        # Initialize data
        from PLAYER_STATS import PLAYER_STATS                              

        self.player_stats = {}

        # 1. Initialize everyone with 0s
        for player in PLAYER_VIDEOS.keys():
            self.player_stats[player] = {col: 0 for col in self.STAT_COLUMNS[1:]}

        # 2. Overwrite only the ones that appear in PLAYER_STATS
        for player, stats in PLAYER_STATS.items():
            if player in self.player_stats:
                self.player_stats[player].update(stats)

        


        # Draft state
        self.teams = []
        self.n_teams = 0
        self.draft_board = []
        self.picked_players = set()
        self.current_pick = 0
        self.draft_started = False
        
        # UI components
        self.draft_labels = []
        self.available_window = None
        self.stats_window = None
        
        # Animation variables
        self.animation_running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        title_frame = GradientFrame(self.root, relief='flat', bd=0)
        title_frame.pack(fill="x", pady=(20, 10))
        
        title_label = tk.Label(
            title_frame, 
            text="⚡ FANTASY FOOTBALL DRAFT PICKER ⚡", 
            font=("Segoe UI", 24, "bold"),
            fg="#60a5fa", 
            bg="#0f172a"
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Build your championship team with style",
            font=("Segoe UI", 12, "italic"),
            fg="#94a3b8",
            bg="#0f172a"
        )
        subtitle_label.pack()
        
        setup_container = GradientFrame(self.root, color1='#1e293b', color2='#0f172a')
        setup_container.pack(fill="x", padx=30, pady=20)
        
        # Left card - Team Setup
        left_card = GradientFrame(setup_container, color1='#374151', color2='#1f2937', relief='raised', bd=2)
        left_card.pack(side="left", padx=20, pady=15, ipadx=25, ipady=15)
        
        card_title = tk.Label(
            left_card,
            text="🏈 Draft Setup",
            font=("Segoe UI", 14, "bold"),
            fg="#f9fafb",
            bg="#374151"
        )
        card_title.pack(pady=(0, 10))
        
        team_frame = tk.Frame(left_card, bg="#374151")
        team_frame.pack(pady=5)
        
        tk.Label(
            team_frame, 
            text="Teams (even numbers only):", 
            font=("Segoe UI", 10),
            fg="#d1d5db", 
            bg="#374151"
        ).pack()
        
        self.team_spinbox = tk.Spinbox(
            team_frame,
            from_=2, to=20, increment=2, width=8,
            bg="#4b5563", fg="#f9fafb", insertbackground="#f9fafb",
            font=("Segoe UI", 11, "bold"),
            relief='flat', bd=0,
            buttonbackground="#6b7280",
            highlightthickness=2,
            highlightcolor="#3b82f6"
        )
        self.team_spinbox.pack(pady=8)
        self.team_spinbox.delete(0, tk.END)
        self.team_spinbox.insert(0, "8")
        
        button_frame = tk.Frame(left_card, bg="#374151")
        button_frame.pack(pady=10)
        
        self.start_button = AnimatedButton(
            button_frame,
            text="🚀 Start Draft",
            command=self.start_draft,
            normal_bg='#10b981',
            hover_bg='#059669',
            active_bg='#047857'
        )
        self.start_button.pack(pady=3)
        
        self.available_button = AnimatedButton(
            button_frame,
            text="👥 Available Players",
            command=self.show_available_players,
            normal_bg='#3b82f6',
            hover_bg='#2563eb',
            active_bg='#1d4ed8'
        )
        self.available_button.pack(pady=3)
        
        self.stats_button = AnimatedButton(
            button_frame,
            text="📊 Player Stats",
            command=self.show_stats,
            normal_bg='#8b5cf6',
            hover_bg='#7c3aed',
            active_bg='#6d28d9'
        )
        self.stats_button.pack(pady=3)
        
        # Right card - Draft Controls
        right_card = GradientFrame(setup_container, color1='#374151', color2='#1f2937', relief='raised', bd=2)
        right_card.pack(side="right", padx=20, pady=15, ipadx=25, ipady=15)
        
        controls_title = tk.Label(
            right_card,
            text="🎯 Draft Controls",
            font=("Segoe UI", 14, "bold"),
            fg="#f9fafb",
            bg="#374151"
        )
        controls_title.pack(pady=(0, 10))
        
        # Next pick
        self.next_pick_label = tk.Label(
            right_card,
            text="⏰ Next Pick: —",
            font=("Segoe UI", 12, "bold"),
            fg="#fbbf24",
            bg="#374151"
        )
        self.next_pick_label.pack(pady=5)
        
        pick_frame = tk.Frame(right_card, bg="#374151")
        pick_frame.pack(pady=15)
        
        tk.Label(
            pick_frame,
            text="Enter Player Name:",
            font=("Segoe UI", 10, "bold"),
            fg="#d1d5db",
            bg="#374151"
        ).pack()
        
        self.player_entry = ModernEntry(pick_frame, width=25)
        self.player_entry.pack(pady=8)
        self.player_entry.bind("<Return>", lambda e: self.make_pick())
        
        self.make_pick_button = AnimatedButton(
            pick_frame,
            text="🏆 DRAFT PLAYER",
            command=self.make_pick,
            normal_bg='#dc2626',
            hover_bg='#b91c1c',
            active_bg='#991b1b',
            font=('Segoe UI', 11, 'bold')
        )
        self.make_pick_button.pack(pady=5)
        
        self.status_label = tk.Label(
            right_card,
            text="",
            font=("Segoe UI", 9),
            fg="#a3a3a3",
            bg="#374151",
            wraplength=250
        )
        self.status_label.pack(pady=8)
        
        board_container = GradientFrame(self.root, color1='#1f2937', color2='#111827', relief='raised', bd=3)
        board_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        board_title = tk.Label(
            board_container,
            text="📋 DRAFT BOARD",
            font=("Segoe UI", 16, "bold"),
            fg="#f9fafb",
            bg="#1f2937"
        )
        board_title.pack(pady=(15, 10))
        
        self.board_frame = tk.Frame(board_container, bg="#111827", relief="flat", bd=0)
        self.board_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
   
        self.board_frame.grid_rowconfigure(0, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbars
        self.canvas = tk.Canvas(self.board_frame, bg="#111827", highlightthickness=0)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Vertical.TScrollbar", 
                       background="#4b5563",
                       troughcolor="#1f2937",
                       bordercolor="#6b7280",
                       arrowcolor="#d1d5db",
                       darkcolor="#374151",
                       lightcolor="#6b7280")
        
        self.scrollbar_v = ttk.Scrollbar(self.board_frame, orient="vertical", command=self.canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollbar_h = ttk.Scrollbar(self.board_frame, orient="horizontal", command=self.canvas.xview, style="Custom.Horizontal.TScrollbar")
        self.scrollable_frame = tk.Frame(self.canvas, bg="#111827")
        
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_v.grid(row=0, column=1, sticky="ns")
        self.scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
    
    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def animate_pick_flash(self, label):
        """Animate the newly picked player with a flash effect"""
        original_bg = label.cget('bg')
        flash_colors = ['#fbbf24', '#f59e0b', '#d97706', '#b45309', original_bg]
        
        def flash_step(step=0):
            if step < len(flash_colors):
                label.config(bg=flash_colors[step])
                self.root.after(200, lambda: flash_step(step + 1))
        
        flash_step()
    
    def start_draft(self):
        try:
            n_teams = int(self.team_spinbox.get())
            if n_teams % 2 != 0:
                messagebox.showerror("⚠️ Error", "Number of teams must be even!")
                return
            
            self.n_teams = n_teams
            
            team_names = []
            for i in range(n_teams):
                name = simpledialog.askstring(
                    "🏈 Team Names", 
                    f"Enter name for Team {i+1}\n(Leave blank for 'Team {i+1}'):",
                    initialvalue=f"Team {i+1}"
                )
                if name is None:
                    return
                team_names.append(name.strip() if name and name.strip() else f"Team {i+1}")
            
            self.teams = team_names
            self.reset_draft()
            self.create_draft_board()
            self.draft_started = True
            self.update_next_pick()
            self.status_label.config(text="🚀 Draft is live! Select a player to begin.", fg="#10b981")
            
        except ValueError:
            messagebox.showerror("⚠️ Error", "Please enter a valid number of teams!")
    
    def reset_draft(self):
        self.draft_board = [["" for _ in range(self.n_teams)] for _ in range(self.ROUNDS)]
        self.picked_players = set()
        self.current_pick = 0
        self.player_entry.delete(0, tk.END)
        
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.draft_labels = []
    
    def create_draft_board(self):
        round_header = tk.Label(
            self.scrollable_frame,
            text="ROUND",
            font=("Segoe UI", 11, "bold"),
            fg="#f9fafb",
            bg="#374151",
            relief="flat",
            bd=2
        )
        round_header.grid(row=0, column=0, sticky="nsew", padx=2, pady=2, ipady=8)
        
        for col, team_name in enumerate(self.teams):
            team_header = tk.Label(
                self.scrollable_frame,
                text=team_name.upper(),
                font=("Segoe UI", 10, "bold"),
                fg="#f9fafb",
                bg="#4b5563",
                relief="flat",
                bd=2,
                wraplength=140
            )
            team_header.grid(row=0, column=col+1, sticky="nsew", padx=2, pady=2, ipady=8)
        
        self.draft_labels = []
        colors = ['#1f2937', '#111827']  
        
        for round_idx in range(self.ROUNDS):
            row_labels = []
            row_color = colors[round_idx % 2]
            
            round_label = tk.Label(
                self.scrollable_frame,
                text=str(round_idx + 1),
                font=("Segoe UI", 12, "bold"),
                fg="#60a5fa",
                bg="#374151",
                relief="flat",
                bd=1
            )
            round_label.grid(row=round_idx+1, column=0, sticky="nsew", padx=2, pady=1, ipady=12)
            
            # Team picks
            for team_idx in range(self.n_teams):
                label = tk.Label(
                    self.scrollable_frame,
                    text="",
                    font=("Segoe UI", 9, "bold"),
                    fg="#d1d5db",
                    bg=row_color,
                    relief="flat",
                    bd=1,
                    anchor="center",
                    wraplength=140
                )
                label.grid(row=round_idx+1, column=team_idx+1, sticky="nsew", padx=2, pady=1, ipady=12)
                row_labels.append(label)
            
            self.draft_labels.append(row_labels)
        
        # Configure grid weights for perfect scaling
        self.scrollable_frame.grid_rowconfigure(0, weight=1)
        for i in range(1, self.ROUNDS + 1):
            self.scrollable_frame.grid_rowconfigure(i, weight=1)
        
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, self.n_teams + 1):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
        
        self.board_frame.grid_rowconfigure(0, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)
    
    def get_snake_pick_position(self, pick_index):
        round_idx = pick_index // self.n_teams
        idx_in_round = pick_index % self.n_teams
        
        if round_idx % 2 == 0:
            team_idx = idx_in_round
        else:
            team_idx = self.n_teams - 1 - idx_in_round
        
        return round_idx, team_idx
    
    def update_next_pick(self):
        if not self.draft_started or self.current_pick >= self.n_teams * self.ROUNDS:
            self.next_pick_label.config(text="⏰ Next Pick: Draft Complete!", fg="#10b981")
            return
        
        round_idx, team_idx = self.get_snake_pick_position(self.current_pick)
        team_name = self.teams[team_idx]
        self.next_pick_label.config(text=f"⏰ Round {round_idx + 1}: {team_name}", fg="#fbbf24")
    
    def make_pick(self):
        if not self.draft_started:
            self.status_label.config(text="❌ Please start the draft first!", fg="#ef4444")
            return
        
        if self.current_pick >= self.n_teams * self.ROUNDS:
            self.status_label.config(text="🎉 Draft is complete! Great job!", fg="#10b981")
            return
        
        player_name = self.player_entry.get().strip()
        if not player_name:
            self.status_label.config(text="❌ Please enter a player name!", fg="#ef4444")
            return
        
        if player_name in self.picked_players:
            self.status_label.config(text="❌ Player already drafted!", fg="#ef4444")
            return
        
        # Try to play video if available
        if player_name in PLAYER_VIDEOS:
            video_path = resource_path(PLAYER_VIDEOS[player_name])
            if os.path.exists(video_path):
                self.play_video(video_path)
            else:
                messagebox.showwarning("⚠️ Video Missing", f"Video file not found: {PLAYER_VIDEOS[player_name]}")
        else:
            messagebox.showinfo("ℹ️ Info", f"No video mapped for {player_name}")
        
        # Play draft sound
        self.play_draft_sound()
        
        # Update draft board with animation
        round_idx, team_idx = self.get_snake_pick_position(self.current_pick)
        self.draft_board[round_idx][team_idx] = player_name
        
        label = self.draft_labels[round_idx][team_idx]
        label.config(
            text=player_name,
            bg="#059669",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="raised",
            bd=2
        )
        
        # Animate the pick
        self.animate_pick_flash(label)
        
        # Update state
        self.picked_players.add(player_name)
        self.current_pick += 1
        self.player_entry.delete(0, tk.END)
        self.update_next_pick()
        
        if self.current_pick >= self.n_teams * self.ROUNDS:
            self.status_label.config(text="🎉 Draft Complete! Championship time!", fg="#10b981")
            # Celebration effect
            self.celebrate_draft_completion()
        else:
            self.status_label.config(text=f"✅ Drafted {player_name}! Next pick up...", fg="#10b981")
    
    def celebrate_draft_completion(self):
        """Special celebration animation when draft is complete"""
        celebration_colors = ['#10b981', '#059669', '#047857', '#065f46']
        
        def flash_celebration(step=0):
            if step < 6:  # Flash 6 times
                color = celebration_colors[step % len(celebration_colors)]
                self.next_pick_label.config(fg=color)
                self.root.after(300, lambda: flash_celebration(step + 1))
            else:
                self.next_pick_label.config(fg="#10b981")
        
        flash_celebration()
    
    def play_video(self, video_path):
        try:
            system = platform.system()
            if system == "Darwin":
                subprocess.run(["open", video_path])
            elif system == "Windows":
                os.startfile(video_path)
            else:
                subprocess.run(["xdg-open", video_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open video: {str(e)}")
    
    def play_draft_sound(self):
        # TODO: Add sound file path here when available
        pass
    
    def show_available_players(self):
        if self.available_window and self.available_window.winfo_exists():
            self.available_window.lift()
            return
        
        self.available_window = tk.Toplevel(self.root)
        self.available_window.title("👥 Available Players")
        self.available_window.geometry("500x650")
        self.available_window.configure(bg="#0f172a")
        
        # Modern header
        header_frame = GradientFrame(self.available_window, color1='#374151', color2='#1f2937')
        header_frame.pack(fill="x", pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="👥 AVAILABLE PLAYERS",
            font=("Segoe UI", 16, "bold"),
            fg="#60a5fa",
            bg="#374151"
        )
        title_label.pack(pady=15)
        
        instructions = tk.Label(
            header_frame,
            text="💡 Double-click any player to draft them instantly",
            font=("Segoe UI", 10, "italic"),
            fg="#94a3b8",
            bg="#374151"
        )
        instructions.pack(pady=(0, 15))
        
        # Available players list
    def show_available_players(self):
        if self.available_window and self.available_window.winfo_exists():
            self.available_window.lift()
            return
        
        self.available_window = tk.Toplevel(self.root)
        self.available_window.title("👥 Available Players & Stats")
        self.available_window.geometry("1400x800")
        self.available_window.configure(bg="#0f172a")
        
        header_frame = GradientFrame(self.available_window, color1='#374151', color2='#1f2937')
        header_frame.pack(fill="x", pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="👥 AVAILABLE PLAYERS & STATS",
            font=("Segoe UI", 18, "bold"),
            fg="#60a5fa",
            bg="#374151"
        )
        title_label.pack(pady=15)
        
        instructions = tk.Label(
            header_frame,
            text="💡 Double-click any player to draft them instantly • Double-click stat cells to edit",
            font=("Segoe UI", 12, "italic"),
            fg="#94a3b8",
            bg="#374151"
        )
        instructions.pack(pady=(0, 15))
        
        tree_container = GradientFrame(self.available_window, color1='#1f2937', color2='#111827', relief='raised', bd=2)
        tree_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        tree_frame = tk.Frame(tree_container, bg="#1f2937")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        style = ttk.Style()
        style.configure("Available.Treeview", 
                       background="#374151",
                       foreground="#f9fafb",
                       fieldbackground="#374151",
                       borderwidth=0,
                       font=("Segoe UI", 11))
        style.configure("Available.Treeview.Heading",
                       background="#4b5563",
                       foreground="#f9fafb",
                       font=("Segoe UI", 11, "bold"))
        
        self.available_tree = ttk.Treeview(
            tree_frame, 
            columns=self.STAT_COLUMNS[1:], 
            show="tree headings",
            style="Available.Treeview"
        )
        
        self.available_tree.column("#0", width=180, minwidth=150)
        for col in self.STAT_COLUMNS[1:]:
            self.available_tree.column(col, width=110, minwidth=90)
        
        self.available_tree.heading("#0", text="🏈 Player")
        heading_emojis = ["📈", "🎯", "🏃", "🙌", "💪", "🎯", "🏃", "🏆", "🙌", "🎯", "💥", "😬", "🎯", "💥","🏟️","🧍","📊","⚡","📅", "📅", "📅","💎" ]
        for i, col in enumerate(self.STAT_COLUMNS[1:]):
            emoji = heading_emojis[i] if i < len(heading_emojis) else "📊"
            self.available_tree.heading(col, text=f"{emoji} {col}")
        
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.available_tree.yview, style="Custom.Vertical.TScrollbar")
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.available_tree.xview, style="Custom.Horizontal.TScrollbar")
        self.available_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.available_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        self.available_tree.bind("<Double-Button-1>", self.available_tree_double_click)
        
        # Populate with available players and their stats
        self.populate_available_stats()
        
        # Close button
        close_button = AnimatedButton(
            self.available_window,
            text="✖️ Close",
            command=self.available_window.destroy,
            normal_bg='#d1d5db',
            hover_bg='#9ca3af',
            active_bg='#6b7280'
        )
        close_button.pack(pady=20)
    
    def populate_available_stats(self):
        """Populate available players tree with all their stats"""
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)
        
        available_players = [p for p in PLAYER_VIDEOS.keys() if p not in self.picked_players]

        ordered = sorted(
            available_players,
            key=lambda p: self.player_stats[p].get("ADP", 9999)  # put missing ADP at end
        )

        for i, player in enumerate(ordered):
            values = [self.player_stats[player][col] for col in self.STAT_COLUMNS[1:]]
            self.available_tree.insert("", "end", text=f"⭐ {player}", values=values)

    def available_tree_double_click(self, event):
        """Handle double-click on available players tree - draft player or edit stat"""
        selection = self.available_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        column = self.available_tree.identify_column(event.x)
        
        # If clicking on player name column, draft the player
        if column == "#0":
            player_text = self.available_tree.item(item, "text")
            player_name = player_text.replace("⭐ ", "")
            
            self.player_entry.delete(0, tk.END)
            self.player_entry.insert(0, player_name)
            self.make_pick()
            
            if self.available_window and self.available_window.winfo_exists():
                self.available_window.destroy()
        else:
            # Edit stat cell
            self.edit_stat_cell(item, column, self.available_tree, is_available_window=True)
    
    def edit_stat_cell(self, item, column, tree_widget, is_available_window=False):
        """Generic stat cell editing for both windows"""
        col_index = int(column.replace("#", "")) - 1
        col_name = self.STAT_COLUMNS[col_index + 1]
        
        player_text = tree_widget.item(item, "text")
        player_name = player_text.replace("⭐ ", "")
        current_value = self.player_stats[player_name][col_name]
        
        bbox = tree_widget.bbox(item, column)
        if not bbox:
            return
        
        x, y, width, height = bbox
        
        # Enhanced edit entry
        edit_entry = tk.Entry(
            tree_widget, 
            width=10,
            bg="#60a5fa",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            bd=0,
            justify="center"
        )
        edit_entry.place(x=x, y=y, width=width, height=height)
        edit_entry.insert(0, str(current_value))
        edit_entry.select_range(0, tk.END)
        edit_entry.focus()
        
        def save_edit(event=None):
            try:
                new_value = edit_entry.get()
                try:
                    new_value = float(new_value)
                    if new_value.is_integer():
                        new_value = int(new_value)
                except ValueError:
                    pass
                
                self.player_stats[player_name][col_name] = new_value
                
                values = list(tree_widget.item(item, "values"))
                values[col_index] = new_value
                tree_widget.item(item, values=values)
                
            except Exception:
                pass
            
            edit_entry.destroy()
        
        def cancel_edit(event=None):
            edit_entry.destroy()
        
        edit_entry.bind("<Return>", save_edit)
        edit_entry.bind("<FocusOut>", save_edit)
        edit_entry.bind("<Escape>", cancel_edit)
    
    def show_stats(self):
        if self.stats_window and self.stats_window.winfo_exists():
            self.stats_window.lift()
            return
        
        self.stats_window = tk.Toplevel(self.root)
        self.stats_window.title("📊 Player Statistics")
        self.stats_window.geometry("1200x700")
        self.stats_window.configure(bg="#0f172a")
        
        header_frame = GradientFrame(self.stats_window, color1='#374151', color2='#1f2937')
        header_frame.pack(fill="x", pady=(20, 15))
        
        title_label = tk.Label(
            header_frame,
            text="📊 PLAYER STATISTICS",
            font=("Segoe UI", 16, "bold"),
            fg="#8b5cf6",
            bg="#374151"
        )
        title_label.pack(pady=15)
        
        instructions = tk.Label(
            header_frame,
            text="💡 Double-click any stat cell to edit • Only showing remaining players",
            font=("Segoe UI", 10, "italic"),
            fg="#94a3b8",
            bg="#374151"
        )
        instructions.pack(pady=(0, 15))
        
        # Button frame
        button_frame = tk.Frame(self.stats_window, bg="#0f172a")
        button_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        refresh_button = AnimatedButton(
            button_frame,
            text="🔄 Refresh",
            command=self.refresh_stats,
            normal_bg='#3b82f6',
            hover_bg='#2563eb',
            active_bg='#1d4ed8'
        )
        refresh_button.pack(side="left")
        
        close_button = AnimatedButton(
            button_frame,
            text="✖️ Close",
            command=self.stats_window.destroy,
            normal_bg='#6b7280',
            hover_bg='#4b5563',
            active_bg='#374151'
        )
        close_button.pack(side="right")
        
        tree_container = GradientFrame(self.stats_window, color1='#1f2937', color2='#111827', relief='raised', bd=2)
        tree_container.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        tree_frame = tk.Frame(tree_container, bg="#1f2937")
        tree_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        style = ttk.Style()
        style.configure("Modern.Treeview", 
                       background="#374151",
                       foreground="#f9fafb",
                       fieldbackground="#374151",
                       borderwidth=0,
                       font=("Segoe UI", 12))  
        style.configure("Modern.Treeview.Heading",
                       background="#4b5563",
                       foreground="#f9fafb",
                       font=("Segoe UI", 12, "bold"))  
        
       
        self.available_tree = ttk.Treeview(
            tree_frame, 
            columns=self.STAT_COLUMNS[1:], 
            show="tree headings",
            style="Available.Treeview"
        )
        
       
        self.available_tree.column("#0", width=200, minwidth=180)
        for col in self.STAT_COLUMNS[1:]:
            self.available_tree.column(col, width=120, minwidth=100)
        
       
        self.available_tree.heading("#0", text="🏈 Player")
        heading_emojis = ["📈", "🎯", "🏃", "🙌", "💪", "🎯", "🏃", "🏆", "🙌", "🎯", "💥", "😬", "🎯", "💥"]
        for i, col in enumerate(self.STAT_COLUMNS[1:]):
            emoji = heading_emojis[i] if i < len(heading_emojis) else "📊"
            self.available_tree.heading(col, text=f"{emoji} {col}")
        
      
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.available_tree.yview, style="Custom.Vertical.TScrollbar")
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.available_tree.xview, style="Custom.Horizontal.TScrollbar")
        self.available_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
       
        self.available_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
     
        self.available_tree.bind("<Double-Button-1>", self.available_tree_double_click)
        
     
        self.populate_available_stats()
        
        # Close button
        close_button = AnimatedButton(
            self.available_window,
            text="✖️ Close",
            command=self.available_window.destroy,
            normal_bg='#d1d5db',
            hover_bg='#9ca3af',
            active_bg='#6b7280'
        )
        close_button.pack(pady=20)
    
    def populate_stats(self):
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        available_players = [p for p in PLAYER_VIDEOS.keys() if p not in self.picked_players]
        
        for i, player in enumerate(sorted(available_players)):
            values = [self.player_stats[player][col] for col in self.STAT_COLUMNS[1:]]
            item = self.stats_tree.insert("", "end", text=f"⭐ {player}", values=values)
            # Alternate row colors
            if i % 2 == 0:
                self.stats_tree.set(item, "#0", f"⭐ {player}")
    
    def refresh_stats(self):
        if hasattr(self, 'stats_tree'):
            self.populate_stats()
    
    def on_stats_double_click(self, event):
        """Handle double-click on stats window"""
        selection = self.stats_tree.selection()
        if not selection:
            return
        item = selection[0]
        column = self.stats_tree.identify_column(event.x)
        
        if column == "#0":
            return
        
        self.edit_stat_cell(item, column, self.stats_tree, is_available_window=False)

def main():
    root = tk.Tk()

    try:
        root.tk.call('tk', 'scaling', 1.5)
    except:
        pass

    try:
        if platform.system() == "Windows":
            root.iconbitmap(default=resource_path("icon.ico"))
        elif platform.system() == "Darwin":
            root.iconbitmap(resource_path("icon.icns"))
    except:
        pass
    
    app = FantasyDraftApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
