# 🔐 Aegis Scan

**AI-Powered Web Application Vulnerability Scanner**

Aegis Scan is an AI-augmented vulnerability scanning and analysis tool that integrates the powerful OWASP ZAP engine with a machine-learning layer for intelligent detection and prioritization of web security flaws.

Currently presented at **BlackHat MEA 2024**, Aegis Scan is being actively enhanced to become an industry-grade open-source project for secure-by-design web applications.

---

## 🚀 Features

- ✅ **AI-Powered Detection**  
  Basic ML model identifies and prioritizes vulnerabilities based on patterns in intercepted HTTP requests. *(Advanced version in progress)*

- ✅ **Detailed Reporting & Compliance Ready**  
  Generate exportable reports that map to standards like OWASP Top 10, PCI-DSS, and GDPR.

- ✅ **ZAP API Integration**  
  Leverages the OWASP ZAP API for passive, spider, and active scanning workflows.

---

## 🗂 Project Structure

```
aegis-scan-frontend/         # React-based frontend interface (Next.js + Tailwind CSS)
backend/                     # Flask backend handling API requests and ZAP interactions
ml_vuln_prioritization/      # Contains initial AI models and logic for vulnerability scoring
build/                       # Docker scripts for ZAP setup and containerization
nginx/                       # Dockerized NGINX configuration for reverse proxy
```

---

## 🎯 Roadmap

- [ ] Upgrade the ML model for higher precision and fewer false positives
- [ ] Advanced UI enhancements for clarity, UX, and multi-project management
- [ ] Full Burp Suite extension integration for seamless request interception + analysis
- [ ] GCP/AWS integrations for automatic scanning of deployed assets
- [ ] Open-source CI/CD security pipeline integrations
- [ ] Enhanced customization: scan templates, rule tuning, auth injection

---

## 🛠 Tech Stack

- **Frontend:** React (Next.js), Tailwind CSS  
- **Backend:** Flask (Python)  
- **Scanner Engine:** OWASP ZAP (Dockerized)  
- **AI/ML:** TensorFlow, PyTorch  
- **Containerization:** Docker  
- **Proxy:** NGINX

---

## 🤝 Contributing

We are actively working on improving and stabilizing Aegis Scan. Community contributions for model training, bug fixes, or UI/UX feedback are welcome!

---

## 📌 Current Status

🧠 Basic AI model implemented  
🎨 UI improvements in progress  
🧪 Burp Suite Extension (early beta)  
🎯 Goal: Production-grade, open-source security tool for researchers and developers

---

## 📜 License

This project is licensed under the GNU General Public License (GPL).

---

## 👥 Credits

Developed by [Simardeep Singh](https://www.linkedin.com/in/simardeepsingh99/) and [Anikait](https://www.linkedin.com/in/anikait-sabharwal/)  
Special thanks to **Nameesha Shetty** for conference support during **BlackHat MEA 2024**.
