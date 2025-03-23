# 📊 Customer Behavior Analytics System

**Description:**  
This project is a **real-time customer behavior analytics system** that captures, processes, and visualizes customer activity data using **Kafka, MongoDB, and Streamlit**. It streams customer click data, stores it in MongoDB, and displays interactive insights on a Streamlit dashboard.

---

## 🚀 Tech Stack
- **Data Streaming:** Kafka (Confluent Cloud)  
- **Database:** MongoDB Atlas  
- **Frontend Visualization:** Streamlit  
- **Backend:** Python (Producer & Consumer)

---

## 🔥 Key Features

### 1️⃣ **Real-time Data Streaming**
- Kafka Producer sends customer activity events to the Kafka topic.  
- Kafka Consumer reads the data, converts timestamps, and inserts it into MongoDB.  

### 2️⃣ **MongoDB Integration**
- Stores customer activity data with efficient querying capabilities.  
- Uses **ISODate format** for consistent timestamp handling.  

### 3️⃣ **Interactive Streamlit Dashboard**
- **Key Metrics:** Total users, activities, and products.  
- **Activity Timeline:** Line graph showing daily activity trends.  
- **Product Distribution:** Pie chart visualizing customer preferences.  
- **User Activity Patterns:** Bar chart for top 10 active users.  

