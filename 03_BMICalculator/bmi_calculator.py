import tkinter as tk
from tkinter import ttk, messagebox

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator Pro")
        self.root.geometry("800x650")
        self.root.minsize(700, 650)
        self.root.configure(bg='#f0f0f0')

        self.weight_var, self.height_var = tk.StringVar(), tk.StringVar()

        self.setup_styles()
        self.setup_ui()
        self.center_window()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Segoe UI', 28, 'bold'), foreground='#2c3e50', background='#f0f0f0')
        style.configure('Heading.TLabel', font=('Segoe UI', 14, 'bold'), foreground='#34495e', background='white')
        style.configure('Info.TLabel', font=('Segoe UI', 11), foreground='#5d6d7e', background='white')
        style.configure('Custom.TEntry', font=('Segoe UI', 12), fieldbackground='white', relief='solid')
        style.configure('Primary.TButton', font=('Segoe UI', 12, 'bold'), foreground='white', background='#3498db')
        style.map('Primary.TButton', background=[('active', '#2980b9'), ('pressed', '#21618c')])

    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x, y = (self.root.winfo_screenwidth() // 2 - w // 2), (self.root.winfo_screenheight() // 2 - h // 2)
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def setup_ui(self):
        main = tk.Frame(self.root, bg='#f0f0f0'); main.pack(fill='both', expand=True, padx=30, pady=20)

        # Header
        ttk.Label(main, text="BMI Calculator", style='Title.TLabel').pack()
        tk.Label(main, text="Track your health with BMI insights", font=('Segoe UI', 11), fg='#7f8c8d', bg='#f0f0f0').pack(pady=5)

        content = tk.Frame(main, bg='#f0f0f0'); content.pack(fill='both', expand=True)

        # Left panel (Inputs)
        left = tk.Frame(content, bg='white', relief='solid', borderwidth=1); left.pack(side='left', expand=True, fill='both', padx=(0,15))
        self.build_inputs(left)

        # Right panel (Results)
        right = tk.Frame(content, bg='white', relief='solid', borderwidth=1); right.pack(side='right', expand=True, fill='both')
        self.results_display = tk.Frame(right, bg='#f8f9fa', relief='solid', borderwidth=1)
        self.results_display.pack(padx=25, pady=25, fill='x')
        self.setup_placeholder()

        # BMI Categories Info
        ttk.Label(right, text="BMI Categories", style='Heading.TLabel').pack(anchor='w', padx=25)
        categories = [("Underweight","<18.5","#3498db"),("Normal","18.5–24.9","#27ae60"),
                      ("Overweight","25–29.9","#f39c12"),("Obese","≥30","#e74c3c")]
        for c,r,color in categories:
            f = tk.Frame(right,bg='white'); f.pack(anchor='w', padx=25, pady=2)
            tk.Frame(f,bg=color,width=4,height=20).pack(side='left', padx=(0,10))
            tk.Label(f,text=f"{c}: {r}",font=('Segoe UI',11),fg='#2c3e50',bg='white').pack(side='left')

        self.root.bind('<Return>', lambda e: self.calculate_bmi())

    def build_inputs(self, parent):
        frame = tk.Frame(parent, bg='white'); frame.pack(padx=25, pady=25, fill='x')
        ttk.Label(frame, text="Enter Your Details", style='Heading.TLabel').pack(anchor='w', pady=10)

        for label, var, unit in [("Weight", self.weight_var, "kg"), ("Height", self.height_var, "cm")]:
            f = tk.Frame(frame,bg='white'); f.pack(fill='x', pady=8)
            ttk.Label(f,text=label,style='Info.TLabel').pack(anchor='w')
            c = tk.Frame(f,bg='white'); c.pack(fill='x')
            ttk.Entry(c,textvariable=var,style='Custom.TEntry',width=15).pack(side='left')
            tk.Label(c,text=f" {unit}",font=('Segoe UI',12),fg='#7f8c8d',bg='white').pack(side='left')

        ttk.Button(frame,text="🧮 Calculate BMI",command=self.calculate_bmi,style='Primary.TButton').pack(fill='x',pady=5)
        ttk.Button(frame,text="🗑️ Clear",command=self.clear_inputs).pack(fill='x')

    def setup_placeholder(self):
        for w in self.results_display.winfo_children(): w.destroy()
        tk.Label(self.results_display,text="Your BMI will appear here",font=('Segoe UI',14),fg='#bdc3c7',bg='#f8f9fa').pack(pady=30)

    def calculate_bmi(self):
        try:
            w, h = float(self.weight_var.get()), float(self.height_var.get())
            if not (0<w<1000 and 0<h<300): raise ValueError
            bmi = round(w/((h/100)**2),1)
            category,color = (("Underweight","#3498db") if bmi<18.5 else
                              ("Normal","#27ae60") if bmi<25 else
                              ("Overweight","#f39c12") if bmi<30 else
                              ("Obese","#e74c3c"))
            self.update_results(bmi, category, color)
        except: messagebox.showerror("Error","Please enter valid weight/height.")

    def update_results(self, bmi, category, color):
        for w in self.results_display.winfo_children(): w.destroy()
        f = tk.Frame(self.results_display,bg=color); f.pack(expand=True,fill='both')
        tk.Label(f,text="Your BMI",font=('Segoe UI',14),fg='white',bg=color).pack()
        tk.Label(f,text=bmi,font=('Segoe UI',36,'bold'),fg='white',bg=color).pack()
        tk.Label(f,text=category,font=('Segoe UI',16),fg='white',bg=color).pack()
        tips={"Underweight":"⚠️ Gain weight with a nutritious diet.",
              "Normal":"✅ Great! Maintain your lifestyle.",
              "Overweight":"⚠️ Exercise & avoid junk food.",
              "Obese":"⚠️ Consult a healthcare provider."}
        tk.Label(f,text="💡 "+tips[category],wraplength=250,fg='#2c3e50',bg='white').pack(pady=10)

    def clear_inputs(self):
        self.weight_var.set(""); self.height_var.set("")
        self.setup_placeholder()

def main():
    root=tk.Tk(); BMICalculator(root); root.mainloop()

if __name__=="__main__": main()
