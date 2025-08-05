# 📁 Excel Manager

**Excel Manager** is a professional-grade, web-based platform for secure and efficient manipulation of Excel and CSV datasets. Designed for analysts, data managers, and business users, the application streamlines routine data tasks—without requiring desktop software like Excel.

---

## 💼 Key Capabilities

- **Multi-file Upload Support**  
  Handle multiple `.xlsx` or `.csv` files simultaneously.

- **Sheet-aware Excel Parsing**  
  Seamlessly switch between sheets in multi-sheet Excel workbooks.

- **Advanced Data Editing**  
  Perform inline edits using an AG-Grid-powered interface.

- **Smart Filtering & Sorting**  
  Filter by column type (text, categorical, numeric, date) and sort with full control.

- **Global & Attribute-based Search**  
  Search across all text fields or within specific columns dynamically.

- **Data Visualization Enhancements**  
  View stylized data tables with Seaborn-inspired visuals for better readability.

- **Record & Column Management**  
  Add new records or columns with dynamic, context-aware input forms.

- **Excel Export & Session Memory**  
  Download modified datasets and preserve app state across interactions.

---

## 🌐 Use Cases

- Internal team dashboards for finance, HR, or operations  
- Lightweight cloud alternative to Excel for quick reviews and edits  
- Educational data projects, staking logs, and business reporting  
- Rapid prototyping of data flows or table-based workflows

---

## 🔒 Privacy & Usability

All processing occurs in-browser or on secure servers, with no third-party data sharing. Designed to minimize friction and maximize productivity, Excel Manager is ideal for users who want a simple yet powerful spreadsheet interface in the cloud.

---

## 📦 Installation

1. Clone the repository and install dependencies:

```bash
git clone https://github.com/Dharshiniramdj/Excel-manager.git
cd bl05OG
pip install -r requirements.txt
```

2. Run the app :

```bash
streamlit run bl05OG.py
```

---

## 📁 File Structure

```
excel-manager/
├── bl05OG.py              
├── requirements.txt        
├── README.md              
├── LICENSE               
└── .gitignore           
```

---

## 📚 Tech Stack

- **Frontend/UI:** Streamlit, st-aggrid
- **Data Handling:** Pandas, OpenPyXL
- **Styling:** Seaborn for DataFrame visuals

---

## 📄 License

This project is licensed under the MIT License.

---

## 👩‍💻 Author

**Dharshini Ram**  
_Data enthusiast and software developer building smart, accessible tools for real-world data workflows._
