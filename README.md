# THackel-Dashboard

Dashboard สำหรับโครงการ **THackle DataViz Challenge**  
หัวข้อการวิเคราะห์: **รายได้เฉลี่ยต่อเดือนของครัวเรือนในประเทศไทย**

โปรเจกต์นี้พัฒนาขึ้นเพื่อสื่อสารผลการวิเคราะห์ข้อมูล Open Data ผ่านทั้ง  
1. **Data Storytelling Notebook** สำหรับอธิบายขั้นตอนการวิเคราะห์อย่างเป็นระบบ  
2. **Interactive Dashboard ด้วย Streamlit** สำหรับสำรวจ insight ในรูปแบบโต้ตอบ

---

## Project Objective

วิเคราะห์ข้อมูลรายได้เฉลี่ยต่อเดือนของครัวเรือนในประเทศไทย เพื่อค้นหา insight ที่สำคัญใน 3 ประเด็นหลัก ได้แก่

1. **Who earns what?**  
   กลุ่มอาชีพใดมีรายได้เฉลี่ยสูงที่สุด และกลุ่มใดมีรายได้ต่ำที่สุด

2. **Where is inequality?**  
   จังหวัดใดมีลักษณะความเหลื่อมล้ำด้านรายได้ภายในพื้นที่เด่นชัด

3. **What is the income structure?**  
   แต่ละกลุ่มอาชีพพึ่งพาแหล่งรายได้ใดเป็นหลัก และกลุ่มใดมีโครงสร้างรายได้เปราะบาง

---

## Data Source

แหล่งข้อมูล: **สำนักงานสถิติแห่งชาติ (National Statistical Office: NSO)**  
เผยแพร่ผ่าน: **Open Government Data of Thailand**

ชุดข้อมูลที่ใช้ในโปรเจกต์นี้ประกอบด้วย

- `avg_income.csv`  
  ใช้สำหรับวิเคราะห์รายได้เฉลี่ยตามกลุ่มอาชีพและแหล่งที่มาของรายได้

- `pct_house.csv`  
  ใช้สำหรับวิเคราะห์การกระจายตัวของครัวเรือนในแต่ละช่วงรายได้

---

## Repository Structure

```text
THackel-Dashboard/
├── app.py
├── requirements.txt
├── avg_income.csv
├── pct_house.csv
└── README.md