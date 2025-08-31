# 📁 Excel Manager

**Excel Manager** is a modern, Streamlit-based web app for managing Excel and CSV datasets. It empowers users to upload, edit, filter, sort, and download spreadsheets—all within an interactive and browser-based interface. No desktop Excel software required.  

---

## 🚀 Features

- **📂 Multi-file Upload** – Work with multiple `.xlsx` and `.csv` files at once.  
- **📑 Sheet-aware Navigation** – Select and view sheets from multi-sheet Excel workbooks.  
- **📄 Styled Data View** – Display DataFrames with gradient highlights for better readability.  
- **✏️ Inline Editing** – Edit table cells directly using an AG-Grid-powered editor.  
- **➕ Add Records & Columns** – Expand datasets with new rows or columns dynamically.  
- **🔍 Smart Search Tools**  
  - Global text search across all columns  
  - Attribute-based column filtering (text, categorical, numeric, date)  
- **↕ Sorting Tool** – Sort any column in ascending/descending order.  
- **📥 Export** – Save and download modified data back to Excel.  

---

## 🌐 Use Cases

- Finance, HR, or operations teams maintaining shared datasets  
- Cloud-based alternative to Excel for quick reviews and edits  
- Educational or research projects requiring lightweight data handling  
- Business reporting dashboards and prototype workflows  

---

## 🔒 Privacy & Security

- All processing happens **locally in the browser or server environment**  
- No third-party sharing of your data  
- Designed for simplicity, speed, and secure handling of spreadsheets  

---

## ⚡ Installation

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/Dharshiniramdj/Excel-manager.git
cd excel-manager
pip install -r requirements.txt
```

2. Run the app:

```bash
streamlit run excel_manager.py
```

---

## 📂 Project Structure

```
excel-manager/
├── excel_manager.py        # Main Streamlit app
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
├── LICENSE                 # License file
└── .gitignore              # Ignored files
```

---

## 🛠️ Tech Stack

- **Framework:** Streamlit  
- **Data Processing:** Pandas, OpenPyXL  
- **UI & Editing:** st-aggrid  
- **Styling:** Seaborn-inspired DataFrame visuals  

---

## 📄 License

Licensed under the MIT License.  

---

## 👩‍💻 Author

**Dharshini Ram**  
_Data enthusiast & developer passionate about building smart, accessible tools for real-world data workflows._  
