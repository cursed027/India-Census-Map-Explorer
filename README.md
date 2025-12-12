---

# India Census Map Explorer

### *A Streamlit + Plotly Interactive Dashboard for District-Level Census 2011 Analysis*

---

## 📌 **Overview**

This project is a minimal, interactive data exploration tool built using **Streamlit**, **Plotly**, and **Pandas**.
It allows users to visualize and compare key socio-economic indicators of **Indian districts** using the Census 2011 dataset.

The app provides:

* 🎯 District-level interactive map
* 🧮 Summary metrics (literacy, sex ratio, penetration rates)
* 📊 Top-districts bar chart
* 🔎 Clean filter/search interface
* 📄 Data preview table

---

## 🚀 **Features**

### 🗺️ **Interactive District Map**

* Plotly Mapbox scatter map
* Adjustable point size and color based on census metrics
* Hover tooltips showing selected district details
* Beautiful color scales (`Viridis`, `Plasma`)

### 🎛️ **Filters & Options**

* View **all India** or filter by **state**
* Select **primary (size)** and **secondary (color)** metrics
* Search any district by name
* Optional **log-scale** coloring

### 📈 **Top 10 Districts Bar Chart**

Shows the highest values for the chosen metric (descending order).
Helpful for identifying best-performing districts.

### 📑 **Data Preview**

Displays the filtered dataset
Useful for quick verification and exploring exact numeric values.

### 🔢 **Automatically Computed Metrics**

* **Sex Ratio** (Females per 1000 Males)
* **Internet Penetration %** (computed if missing)

---

## 📂 **Project Structure**

```
📁 mini_proj/
│── app.py
│── README.md
│── final_india.csv
```

---

## 🧠 **Dataset Description**

This app uses a cleaned version of District-Level India Census 2011 containing:

### **Demographics**

* Population, Male, Female
* SC / ST population

### **Literacy**

* Literate population (Male/Female)
* Literacy Rate (%)

### **Household & Amenities**

* Electricity, Internet, Computer
* LPG/PNG availability
* Bathroom / Toilet availability

### **Assets**

* Bicycle, Car, Two-Wheeler
* Phone, TV

### **Age Groups**

* 0–29
* 30–49
* 50+

### **Geolocation**

* Latitude
* Longitude

### **Derived Metrics**

* Sex_Ratio
* Internet_Penetration

---

## 🛠️ **Installation & Setup**

### 1️⃣ Clone Repository

```bash
git clone https://github.com/cursed027/India-Census-Map-Explorer/
cd india-census-map-explorer
```

### 2️⃣ Install Required Packages

```bash
pip install streamlit pandas numpy plotly
```

### 3️⃣ Run the App

```bash
streamlit run app.py
```

### 4️⃣ Access in Browser

Streamlit will open automatically, or visit:

```
http://localhost:8501
```

---

## 🖥️ **How the App Works**

### 1. Load Dataset

The CSV is automatically loaded from:

```
final_india.csv
```

### 2. Sidebar Options

Choose:

* State
* Primary metric (point size)
* Secondary metric (color)
* Log-scale option
* District search

### 3. Map Rendering

Each district is shown as a point on the India map using:

* Size → selected primary metric
* Color → selected secondary metric

### 4. Insights

* Key performance indicators (KPIs)
* Top 10 districts bar chart
* Filtered data preview

---

## 📊 **Screenshots**

(Insert your images later)

```
![Map View](assets/map.png)
![Bar Chart](assets/top10.png)
```

---

## 🧰 **Tech Stack**

| Component       | Technology                   |
| --------------- | ---------------------------- |
| Dashboard       | Streamlit                    |
| Plots           | Plotly Express               |
| Data Processing | Pandas, NumPy                |
| Map Tiles       | Mapbox (OpenStreetMap style) |

---

## 🔮 **Future Improvements**

* Add choropleth maps using district GeoJSON
* Support multiple census years
* Add download/export options
* Add scatter comparison (primary vs secondary)
* Dark mode UI

---

## 📜 **License**

MIT License — you are free to use and modify the code.

---

## 👨‍💻 **Author**

**Cursed027**

---

