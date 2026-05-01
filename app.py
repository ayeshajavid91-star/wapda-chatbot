from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Knowledge base for WAPDA MDC chatbot
KNOWLEDGE_BASE = {
    "meter reading": {
        "questions": ["what is meter reading", "how to read meter", "meter reading process", "reading procedure", "how meter reading works"],
        "answer": "📊 **Meter Reading Process in WAPDA:**\n\nAs an MDC, the meter reading process involves:\n\n🔸 **Daily Routine:**\n- Receive assigned meter reading routes\n- Plan daily schedule for efficiency\n- Carry necessary equipment (reader, forms, safety gear)\n\n🔸 **Reading Procedure:**\n- Locate meter box safely\n- Record meter number and reading\n- Note any abnormalities (tampered, faulty, zero reading)\n- Take photos if required\n- Update mobile app/database immediately\n\n🔸 **Data Validation:**\n- Cross-check readings with previous months\n- Identify consumption anomalies\n- Flag suspicious readings for investigation\n\n🔸 **Reporting:**\n- Submit daily reports to supervisor\n- Update central database\n- Handle consumer queries on-site\n\n🔸 **Real-Life Scenarios & Handling:**\n\n🔒 **Locked/Inaccessible Meters:**\n- Attempt to contact consumer for access\n- Note as 'inaccessible' with reason\n- Schedule revisit or coordinate with supervisor\n- Document with photos if possible\n\n🔧 **Faulty/Damaged Meters:**\n- Record condition and take photos\n- Flag for immediate replacement\n- Provide temporary reading if safe\n- Report to maintenance team\n\n🌧️ **Bad Weather Conditions:**\n- Postpone readings in heavy rain/storm\n- Use protective gear for light rain\n- Ensure vehicle and equipment safety\n- Reschedule affected routes\n\n📈 **Unusual Readings:**\n- Verify reading multiple times\n- Check for meter faults or tampering\n- Interview consumer about usage\n- Flag for anomaly investigation\n\n🕵️ **Meter Tampering:**\n- Do not touch or alter evidence\n- Take detailed photos from distance\n- Report immediately to supervisor\n- Initiate legal investigation process\n\n🐕 **Safety Risks:**\n- Assess situation before approaching\n- Use safety protocols for animals\n- Avoid dangerous areas\n- Report unsafe conditions\n- Prioritize personal safety always"
    },
    "mdc": {
        "questions": ["what is mdc", "meter data controller", "mdc role", "mdc responsibilities", "mdc duties", "mdc job"],
        "answer": "👨‍💼 **MDC (Meter Data Controller) - Complete Role Overview:**\n\n**Core Responsibilities:**\n\n🏢 **Office Duties:**\n- Data entry and validation\n- Anomaly detection and reporting\n- Consumer complaint resolution\n- Billing coordination\n- Software maintenance\n\n🏃‍♂️ **Field Duties:**\n- Supervising meter readers\n- Training new staff\n- Equipment maintenance\n- Safety compliance\n- Emergency response\n\n💻 **Technical Skills:**\n- Meter reading software proficiency\n- Database management\n- GPS navigation\n- Mobile applications\n- Report generation\n\n📈 **Key Performance Indicators:**\n- Reading accuracy (98%+ target)\n- Timely submissions\n- Consumer satisfaction\n- Anomaly detection rate\n\n**Daily Operations:**\n\n🌅 **Morning:**\n- Collect and verify meter data from readers\n- Coordinate with billing teams for data sync\n- Resolve discrepancies in readings\n- Handle urgent consumer complaints\n\n🌞 **Day:**\n- Respond to faulty meter reports\n- Investigate abnormal readings\n- Supervise field teams\n- Update system databases\n\n🌆 **Evening:**\n- Compile daily reports\n- Escalate unresolved issues\n- Plan next day's activities\n- Ensure data accuracy\n\n**Coordination:**\n- Work with meter readers for data collection\n- Liaise with billing department for corrections\n- Coordinate with technical teams for repairs\n- Handle consumer inquiries and resolutions\n\n**Career Path:** Usually starts as Meter Reader → Senior Reader → MDC → Senior MDC → Supervisor"
    },
    "wapda": {
        "questions": ["what is wapda", "wapda meaning", "about wapda", "wapda structure", "wapda organization"],
        "answer": "🏛️ **WAPDA (Water and Power Development Authority) - Pakistan's Power Giant:**\n\n**Established:** 1958\n**Headquarters:** Lahore, Pakistan\n**Employees:** 120,000+\n\n**Core Functions:**\n\n⚡ **Power Generation:**\n- Hydropower (70% of generation)\n- Thermal power plants\n- Nuclear energy\n- Renewable energy projects\n\n🌊 **Water Management:**\n- Irrigation systems\n- Dam operations\n- Water resource planning\n\n📊 **Distribution & Billing:**\n- 18 Distribution Companies (DISCOs)\n- Meter reading operations\n- Billing and collection\n- Consumer services\n\n**Organizational Structure:**\n- Chairman/MD\n- Executive Directors\n- General Managers\n- Regional Directors\n- Divisional Heads\n- Field Staff (MDCs, Meter Readers)\n\n**Key Achievements:** World's largest irrigation system, Tarbela Dam, Major hydropower projects"
    },
    "billing": {
        "questions": ["billing process", "how billing works", "bill calculation", "bill generation", "billing cycle", "tariff rates"],
        "answer": "💰 **WAPDA Billing System - Complete Guide:**\n\n**Billing Cycle:** Monthly (1st to 30th/31st)\n\n**Tariff Categories:**\n\n🏠 **Residential:**\n- Single Phase: Rs. 5-20 per unit (slab system)\n- Three Phase: Rs. 15-25 per unit\n\n🏪 **Commercial:**\n- Small: Rs. 18-22 per unit\n- Medium: Rs. 20-24 per unit\n- Large: Rs. 22-26 per unit\n\n🏭 **Industrial:**\n- LT: Rs. 12-18 per unit\n- HT: Rs. 10-15 per unit\n- EHT: Rs. 8-12 per unit\n\n**Bill Components:**\n- Energy Charges (based on units consumed)\n- Fixed Charges (monthly minimum)\n- Electricity Duty\n- TV Fee (if applicable)\n- GST (17%)\n- Late Payment Surcharge (if delayed)\n\n**Payment Methods:**\n- Online banking\n- Mobile apps\n- Utility stores\n- Bank branches\n- ATMs\n\n**Common Issues & Resolution:**\n\n❌ **Incorrect Bills:**\n- Verify meter readings\n- Check tariff application\n- Correct billing data\n- Issue revised bill\n\n💸 **High Charges:**\n- Investigate consumption patterns\n- Inspect for meter faults\n- Review load usage\n- Adjust bill if warranted\n\n📊 **Wrong Readings:**\n- Cross-check with actual meter\n- Correct data entry errors\n- Update system records\n- Re-bill if necessary\n\n🏷️ **Tariff Errors:**\n- Verify consumer category\n- Apply correct tariff rates\n- Recalculate charges\n- Refund overpayments\n\n**Resolution Process:** Coordinate with billing department, verify all data, make corrections, and communicate changes to consumer"
    },
    "meter": {
        "questions": ["meter types", "electric meter", "types of meters", "meter installation", "smart meter", "analog meter"],
        "answer": "⚡ **WAPDA Meter Types - Technical Overview:**\n\n**1. Analog Meters (Traditional):**\n- Mechanical disk rotation\n- Manual reading required\n- Accuracy: ±2%\n- Lifespan: 10-15 years\n\n**2. Digital Meters:**\n- LCD display\n- Automatic reading possible\n- Accuracy: ±1%\n- Lifespan: 15-20 years\n\n**3. Smart Meters (AMI):** \n- Two-way communication\n- Real-time monitoring\n- Remote disconnection\n- Load management\n- Accuracy: ±0.5%\n\n**4. Prepaid Meters:**\n- Pay-as-you-go system\n- Automatic disconnection on zero balance\n- Mobile recharge facility\n\n**Installation Process:**\n- Site survey\n- Safety clearance\n- Meter testing\n- Connection and sealing\n- Consumer education\n- Commissioning\n\n**Maintenance:** Regular calibration, cleaning, replacement of faulty units"
    },
    "consumer": {
        "questions": ["consumer categories", "consumer types", "residential commercial", "connection types"],
        "answer": "👥 **WAPDA Consumer Categories - Detailed Classification:**\n\n**A. Domestic/Residential:**\n- **R-1:** Single phase, up to 5kW load\n- **R-2:** Three phase, 5-15kW load\n- **R-3:** Three phase, above 15kW\n\n**B. Commercial:**\n- **C-1:** Small shops, up to 5kW\n- **C-2:** Medium commercial, 5-15kW\n- **C-3:** Large commercial, above 15kW\n\n**C. Industrial:**\n- **I-1:** Small industry, up to 25kW\n- **I-2:** Medium industry, 25-500kW\n- **I-3:** Large industry, above 500kW\n\n**D. Agricultural:**\n- **A-1:** Tubewell up to 5HP\n- **A-2:** Tubewell 5-10HP\n- **A-3:** Tubewell above 10HP\n\n**E. Special Categories:**\n- Government buildings\n- Educational institutions\n- Religious places\n- Hospitals\n- Street lighting\n\n**Connection Requirements:**\n- Valid CNIC\n- Property documents\n- Load sanction\n- Safety inspection\n- Security deposit"
    },
    "anomaly": {
        "questions": ["meter anomaly", "consumption anomaly", "unusual reading", "tampering", "meter fault"],
        "answer": "🚨 **Meter Anomalies & Investigation Process:**\n\n**Common Anomalies:**\n\n📈 **High Consumption:**\n- Sudden 2-3x increase\n- Continuous high usage\n- Unusual timing patterns\n\n📉 **Low/Zero Reading:**\n- No consumption recorded\n- Meter stopped\n- Reverse rotation\n\n🔧 **Technical Issues:**\n- Faulty meter\n- Loose connections\n- Phase imbalance\n- CT/PT problems\n\n🕵️ **Tampering Signs:**\n- Broken seals\n- Magnetic interference\n- Bypassed connections\n- Altered meter numbers\n\n**Step-by-Step Anomaly Handling:**\n\n1. **Identify Anomaly:**\n   - Review consumption data\n   - Compare with historical patterns\n   - Flag unusual readings\n\n2. **Verify Reading:**\n   - Check meter physically\n   - Take accurate reading\n   - Confirm meter condition\n\n3. **Inspect Meter:**\n   - Look for physical damage\n   - Check seals and connections\n   - Test meter functionality\n\n4. **Check System Data:**\n   - Review billing history\n   - Verify data entry\n   - Cross-reference records\n\n5. **Take Action:**\n   - Repair faulty components\n   - Confirm tampering evidence\n   - Report to authorities if needed\n\n6. **Document Issue:**\n   - Record findings\n   - Take photos\n   - Note all observations\n\n7. **Escalate if Needed:**\n   - Report to supervisor\n   - Involve technical teams\n   - Legal action for tampering\n\n8. **Ensure Resolution:**\n   - Correct billing\n   - Replace equipment\n   - Update consumer records\n   - Close investigation\n\n**MDC Role:** Primary anomaly detector and investigator"
    },
    "dispute": {
        "questions": ["meter dispute", "billing dispute", "meter complaint", "complaint resolution"],
        "answer": "📞 **Consumer Complaint & Dispute Resolution:**\n\n**Common Complaints:**\n\n💡 **Billing Issues:**\n- Incorrect readings\n- Wrong tariff application\n- Calculation errors\n- Duplicate billing\n\n⚡ **Service Problems:**\n- Power outages\n- Low voltage\n- Frequent tripping\n- Meter malfunction\n\n**Resolution Process:**\n\n1. **Registration:**\n   - Call center (121)\n   - Online portal\n   - Local office\n   - Mobile app\n\n2. **Initial Assessment:**\n   - Complaint logging\n   - Priority assignment\n   - MDC assignment\n\n3. **Field Investigation:**\n   - Site visit\n   - Meter inspection\n   - Load checking\n   - Consumer interview\n\n4. **Resolution:**\n   - Bill correction\n   - Meter replacement\n   - Service restoration\n   - Explanation to consumer\n\n5. **Follow-up:**\n   - Consumer feedback\n   - Case closure\n   - Report generation\n\n**MDC Role:** Field investigation and resolution coordination"
    },
    "safety": {
        "questions": ["safety", "safety procedures", "meter reading safety", "electrical safety"],
        "answer": "🛡️ **Safety Protocols for MDC & Meter Readers:**\n\n**Personal Safety:**\n\n👷 **PPE Requirements:**\n- Safety helmet\n- Safety shoes\n- High-visibility vest\n- Insulated gloves\n- Safety glasses\n\n⚡ **Electrical Safety:**\n- Never touch live wires\n- Use proper tools\n- Maintain safe distance\n- Report faulty equipment\n\n🚗 **Vehicle Safety:**\n- Valid license\n- Vehicle maintenance\n- Safe driving practices\n- Emergency kit\n\n🏠 **Field Safety:**\n- Dog safety protocols\n- Weather considerations\n- Night reading precautions\n- Emergency contacts\n\n**Specific Safety Procedures:**\n\n🌧️ **Working in Rain:**\n- Use waterproof gear\n- Avoid slippery surfaces\n- Postpone in heavy storms\n- Keep equipment dry\n\n⚡ **Near Live Wires:**\n- Maintain 3-foot distance\n- Use insulated tools only\n- Report exposed wires\n- Never work alone\n\n🐕 **Aggressive Animals:**\n- Assess situation first\n- Use long-handled tools\n- Keep safe distance\n- Call animal control if needed\n- Never approach threatening animals\n\n**Emergency Procedures:**\n- Accident reporting\n- First aid knowledge\n- Emergency numbers\n- Evacuation plans\n\n**Priority:** Personal safety always comes first. Never compromise safety for completing tasks.\n\n**MDC Responsibility:** Safety training, compliance monitoring, incident reporting"
    },
    "software": {
        "questions": ["software", "meter reading software", "mdc software", "mobile app", "database"],
        "answer": "💻 **WAPDA MDC Software & Tools:**\n\n**Core Systems:**\n\n�️ **MDMS (Meter Data Management System):**\n- Central data repository\n- Reading validation and processing\n- Anomaly detection algorithms\n- Reporting and analytics\n\n💰 **Billing Software:**\n- Automated bill generation\n- Tariff calculation\n- Payment processing\n- Consumer database\n\n📱 **Mobile Applications:**\n- Meter reading app\n- GPS tracking\n- Photo capture\n- Real-time sync\n- Offline capability\n\n🗃️ **CIS (Customer Information System):**\n- Consumer profile management\n- Connection history\n- Complaint tracking\n- Service request processing\n\n**Key Features:**\n\n🔍 **Data Management:**\n- Consumer database\n- Reading history\n- Bill history\n- Payment records\n\n📊 **Analytics:**\n- Consumption patterns\n- Anomaly detection\n- Performance metrics\n- Revenue analysis\n\n📋 **Reporting:**\n- Daily reading reports\n- Monthly summaries\n- Anomaly reports\n- Performance reports\n\n**Common Software Issues & Resolution:**\n\n❌ **System Errors:**\n- Restart application\n- Check network connectivity\n- Update software version\n- Contact IT support\n\n🔄 **Data Sync Problems:**\n- Verify internet connection\n- Retry synchronization\n- Check data integrity\n- Manual data entry if needed\n\n📡 **Connectivity Issues:**\n- Switch to mobile data\n- Find better signal area\n- Use offline mode\n- Sync when connected\n\n📝 **Incorrect Data:**\n- Validate entries\n- Cross-check with physical records\n- Correct errors immediately\n- Report system bugs\n\n**Technical Skills Required:**\n- Mobile app operation\n- Data entry accuracy\n- GPS navigation\n- Basic troubleshooting\n- Report interpretation\n\n**MDC Training:** Software proficiency, data accuracy, system updates"
    },
    "career": {
        "questions": ["career", "mdc career", "job opportunities", "advancement", "salary"],
        "answer": "🚀 **Career Path in WAPDA Meter Reading Division:**\n\n**Entry Level:**\n- **Meter Reader:** Starting position\n- Salary: Rs. 25,000-35,000/month\n- Requirements: Matric/Intermediate\n\n**Mid Level:**\n- **Senior Meter Reader:** 2-3 years experience\n- Salary: Rs. 35,000-45,000/month\n- Additional responsibilities\n\n**Professional Level:**\n- **MDC (Meter Data Controller):** 3-5 years experience\n- Salary: Rs. 45,000-65,000/month\n- Supervisory role\n\n**Senior Level:**\n- **Senior MDC:** 5+ years experience\n- Salary: Rs. 65,000-85,000/month\n- Team leadership\n\n**Management Level:**\n- **Meter Reading Supervisor:** Technical expertise\n- Salary: Rs. 85,000-120,000/month\n- Administrative duties\n\n**Benefits:**\n- Health insurance\n- Pension scheme\n- Annual increments\n- Training opportunities\n- Job security\n\n**Required Skills:**\n- Technical knowledge\n- Communication skills\n- Computer literacy\n- Problem-solving ability\n- Field work capability\n\n**Advancement Path:** Performance-based promotions, additional qualifications, specialized training"
    },
    "power outages": {
        "questions": ["power outage", "power cut", "electricity failure", "load shedding", "power failure", "no electricity"],
        "answer": "⚡ **Power Outages & Restoration Process:**\n\n**Types of Outages:**\n\n🔌 **Planned Outages:**\n- Scheduled maintenance\n- System upgrades\n- Load management\n- Announced in advance\n\n🚨 **Unplanned Outages:**\n- Equipment failure\n- Faults in transmission/distribution\n- Natural disasters\n- Accidents\n\n**Restoration Process:**\n\n1. **Detection & Reporting:**\n   - Automatic monitoring systems\n   - Consumer reports\n   - Field staff alerts\n\n2. **Assessment:**\n   - Fault location identification\n   - Impact assessment\n   - Resource mobilization\n\n3. **Repair & Restoration:**\n   - Emergency response teams\n   - Equipment replacement\n   - System testing\n   - Power restoration\n\n4. **Communication:**\n   - Consumer notifications\n   - Estimated restoration time\n   - Safety warnings\n\n**Consumer Actions:**\n- Report outages immediately\n- Follow safety guidelines\n- Keep emergency lights ready\n- Avoid electrical repairs yourself\n\n**Contact:** Call 121 (WAPDA helpline) or local office"
    },
    "new connections": {
        "questions": ["new connection", "electricity connection", "apply for electricity", "connection process", "load sanction"],
        "answer": "🔌 **New Electricity Connection Process:**\n\n**Step 1: Application**\n- Visit local WAPDA office\n- Submit application form\n- Provide required documents\n- Pay application fee\n\n**Required Documents:**\n- Valid CNIC\n- Property ownership documents\n- Site plan/layout\n- Load requirement details\n- Affidavit (if required)\n\n**Step 2: Survey & Assessment**\n- Technical feasibility check\n- Load calculation\n- Safety inspection\n- Cost estimation\n\n**Step 3: Approval & Payment**\n- Load sanction approval\n- Security deposit payment\n- Connection charges\n- Development charges\n\n**Step 4: Installation**\n- Meter installation\n- Wiring and connection\n- Testing and commissioning\n- Consumer education\n\n**Timeline:** 15-45 days depending on location and load\n\n**Costs:** Vary by category and load (Rs. 5,000-50,000+)\n\n**Contact:** Local WAPDA SDO office or online portal"
    },
    "payment": {
        "questions": ["payment", "pay bill", "payment methods", "online payment", "payment issues", "late payment"],
        "answer": "💳 **Electricity Bill Payment Options:**\n\n**Online Methods:**\n\n🌐 **WAPDA Website:**\n- Register account\n- Pay via credit/debit card\n- Direct bank transfer\n- Mobile wallet integration\n\n📱 **Mobile Apps:**\n- WAPDA official app\n- Bank apps (HBL, UBL, etc.)\n- JazzCash, EasyPaisa\n- PayPal integration\n\n🏦 **Bank Branches:**\n- All major banks\n- Utility bill counters\n- Online banking portals\n\n🏪 **Retail Outlets:**\n- Utility stores\n- ATMs\n- Post offices\n- Authorized agents\n\n**Payment Issues Resolution:**\n\n❌ **Failed Payments:**\n- Check transaction status\n- Contact bank/payment provider\n- Retry payment\n- Report to WAPDA\n\n⏰ **Late Payments:**\n- Surcharge: 1.5% per month\n- Disconnection after 2 months\n- Restoration charges apply\n\n📅 **Due Dates:**\n- Bills due by 15th of following month\n- Grace period: 7 days\n- Late payment surcharge applies after due date\n\n**Contact:** 121 helpline or local office"
    },
    "high bills": {
        "questions": ["high bill", "increased bill", "excessive bill", "bill too high", "unusual bill"],
        "answer": "📈 **High Electricity Bill Investigation:**\n\n**Possible Causes:**\n\n🔌 **Usage Increase:**\n- New appliances\n- Extended usage hours\n- Additional family members\n- Seasonal changes\n\n⚡ **Technical Issues:**\n- Faulty meter\n- Slow meter rotation\n- Connection problems\n- Phase imbalance\n\n🕵️ **Tampering/Suspected Theft:**\n- Illegal connections\n- Meter bypassing\n- Magnetic interference\n\n**Investigation Process:**\n\n1. **Bill Review:**\n   - Compare with previous bills\n   - Check tariff application\n   - Verify meter readings\n\n2. **Field Inspection:**\n   - Meter testing and calibration\n   - Load measurement\n   - Connection inspection\n\n3. **Consumer Interview:**\n   - Usage pattern discussion\n   - Appliance inventory\n   - Billing history review\n\n4. **Resolution:**\n   - Bill correction/adjustment\n   - Meter replacement if faulty\n   - Consumer education\n   - Theft case registration if applicable\n\n**Prevention Tips:**\n- Monitor monthly usage\n- Report issues immediately\n- Keep appliance records\n- Regular meter checks\n\n**Contact:** Call 121 or visit local office"
    },
    "faulty meters": {
        "questions": ["faulty meter", "meter not working", "meter problem", "meter issue", "broken meter"],
        "answer": "🔧 **Faulty Meter Diagnosis & Replacement:**\n\n**Common Meter Faults:**\n\n⏹️ **Stopped Meter:**\n- No disk rotation\n- Zero reading\n- Glass fogged/cracked\n\n🐌 **Slow Meter:**\n- Under-recording consumption\n- Disk rotates slowly\n- Inaccurate readings\n\n⚡ **Fast Meter:**\n- Over-recording consumption\n- Rapid disk rotation\n- Higher than normal bills\n\n🔄 **Erratic Meter:**\n- Inconsistent readings\n- Display problems\n- Electronic faults\n\n**Replacement Process:**\n\n1. **Fault Reporting:**\n   - Consumer complaint\n   - MDC field detection\n   - Automatic monitoring\n\n2. **Investigation:**\n   - Physical inspection\n   - Testing with load\n   - Calibration check\n\n3. **Approval:**\n   - Fault confirmation\n   - Replacement authorization\n   - Cost assessment\n\n4. **Installation:**\n   - Old meter removal\n   - New meter installation\n   - Testing and sealing\n   - Data transfer\n\n5. **Billing Adjustment:**\n   - Previous bill correction\n   - New meter baseline\n   - Consumer notification\n\n**Timeline:** 3-7 working days\n\n**Cost:** Free for WAPDA (consumer pays if tampering detected)\n\n**Contact:** Local WAPDA office or 121 helpline"
    },
    "billing corrections": {
        "questions": ["billing correction", "bill correction", "wrong bill", "incorrect bill", "bill error"],
        "answer": "📝 **Electricity Bill Corrections & Adjustments:**\n\n**Types of Corrections:**\n\n🔢 **Reading Errors:**\n- Wrong meter reading\n- Data entry mistakes\n- Missed readings\n\n🏷️ **Tariff Errors:**\n- Wrong category application\n- Incorrect slab calculation\n- Missing discounts\n\n⚙️ **Technical Adjustments:**\n- Faulty meter corrections\n- Load change adjustments\n- System error corrections\n\n**Correction Process:**\n\n1. **Application:**\n   - Submit correction request\n   - Provide supporting evidence\n   - Pay any outstanding dues\n\n2. **Verification:**\n   - Bill history review\n   - Field investigation\n   - Document verification\n\n3. **Approval:**\n   - Correction calculation\n   - Adjustment amount determination\n   - Approval from authority\n\n4. **Implementation:**\n   - Bill adjustment/reversal\n   - Refund processing\n   - Future bill corrections\n\n5. **Communication:**\n   - Consumer notification\n   - Explanation of changes\n   - Future prevention advice\n\n**Timeline:** 15-30 days\n\n**Supporting Documents:**\n- Previous bills\n- Meter photos\n- Usage records\n- Affidavits if needed\n\n**Contact:** Local billing office or 121 helpline"
    },
    "mdc office": {
        "questions": ["mdc office", "office operations", "coordination", "mepco operations", "office duties"],
        "answer": "🏢 **MDC Office Operations & Coordination:**\n\n**Core Functions:**\n\n📊 **Data Management:**\n- Meter reading data validation\n- Billing data processing\n- Consumer database maintenance\n- Anomaly detection and reporting\n\n👥 **Team Coordination:**\n- Supervising meter readers\n- Coordinating with billing staff\n- Liaising with customer service\n- Working with technical teams\n\n📞 **Consumer Services:**\n- Complaint registration and tracking\n- Bill inquiry resolution\n- Connection request processing\n- Information dissemination\n\n🔧 **Technical Support:**\n- Equipment maintenance scheduling\n- Software troubleshooting\n- System updates and training\n- Technical issue resolution\n\n**Daily Operations:**\n\n🌅 **Morning:**\n- Route assignments to readers\n- Data synchronization\n- Priority task allocation\n\n🌞 **Day:**\n- Real-time monitoring\n- Issue resolution\n- Field support coordination\n\n🌆 **Evening:**\n- Data compilation\n- Report generation\n- Next day planning\n\n**Key Performance Areas:**\n- Data accuracy (99%+)\n- Response time (<24 hours)\n- Consumer satisfaction\n- Operational efficiency\n\n**Tools & Systems:**\n- MDC management software\n- GIS mapping systems\n- Communication platforms\n- Reporting dashboards\n\n**Coordination with MEPCO:**\n- Regional office liaison\n- Policy implementation\n- Resource allocation\n- Performance monitoring"
    }
}

def find_relevant_answer(user_query):
    """Find relevant answer from knowledge base"""
    user_query_lower = user_query.lower()
    
    # Special commands
    if user_query_lower in ['quiz', 'test', 'exam', 'assessment']:
        return start_quiz()
    elif user_query_lower in ['guide', 'tutorial', 'steps', 'how to']:
        return show_guide_menu()
    elif user_query_lower.startswith('guide '):
        guide_topic = user_query_lower.replace('guide ', '')
        return get_guide(guide_topic)
    
    # Check each category
    for category, data in KNOWLEDGE_BASE.items():
        for question_keyword in data["questions"]:
            if question_keyword.lower() in user_query_lower:
                return data["answer"]
    
    # If no match found, return generic response
    return get_fallback_response(user_query)

def start_quiz():
    """Start an interactive quiz"""
    return """🎯 **WAPDA MDC Knowledge Quiz**

Test your knowledge about meter reading and MDC responsibilities!

**Question 1:** What does MDC stand for?
A) Meter Data Controller
B) Monthly Data Checker  
C) Main Distribution Center
D) Meter Device Coordinator

Reply with the letter of your choice (A, B, C, or D) to continue the quiz!"""

def show_guide_menu():
    """Show available step-by-step guides"""
    return """📚 **Step-by-Step Guides Available:**

🔸 **Meter Reading Guide** - Complete field procedure
🔸 **Anomaly Investigation** - How to handle suspicious readings  
🔸 **Consumer Complaint Resolution** - Complaint handling process
🔸 **Safety Procedures** - Field safety protocols
🔸 **Software Usage** - MDC software tutorial

**Usage:** Type "guide [topic]" (e.g., "guide meter reading")"""

def get_guide(topic):
    """Return step-by-step guide for specific topic"""
    guides = {
        "meter reading": """📋 **Complete Meter Reading Guide**

**Step 1: Preparation**
- Check assigned routes
- Prepare equipment (reader, forms, PPE)
- Update mobile app
- Plan efficient route

**Step 2: Field Procedure**
- Locate meter safely
- Record meter number
- Take reading accurately
- Note abnormalities
- Photograph if needed

**Step 3: Data Entry**
- Enter reading in app
- Flag anomalies
- Add consumer notes
- Sync data immediately

**Step 4: Verification**
- Cross-check with previous reading
- Validate data accuracy
- Report issues to supervisor

**Step 5: Completion**
- Submit daily report
- Update central database
- Handle consumer queries
- Prepare for next day""",

        "anomaly": """🔍 **Anomaly Investigation Guide**

**Step 1: Detection**
- Monitor consumption patterns
- Identify unusual readings
- Compare with historical data
- Flag suspicious cases

**Step 2: Initial Assessment**
- Review meter history
- Check for technical issues
- Analyze consumption logic
- Categorize anomaly type

**Step 3: Field Investigation**
- Visit consumer premises
- Inspect meter physically
- Check connections
- Interview consumer

**Step 4: Technical Verification**
- Test meter accuracy
- Check for tampering
- Measure actual load
- Document findings

**Step 5: Resolution**
- Correct bill if needed
- Replace faulty equipment
- Report tampering cases
- Update consumer records""",

        "complaint": """📞 **Consumer Complaint Resolution**

**Step 1: Complaint Registration**
- Log complaint details
- Assign priority level
- Notify relevant MDC
- Set response timeline

**Step 2: Initial Response**
- Contact consumer
- Acknowledge complaint
- Gather preliminary information
- Schedule investigation

**Step 3: Investigation**
- Field visit and inspection
- Technical assessment
- Consumer interview
- Evidence collection

**Step 4: Resolution**
- Determine root cause
- Implement corrective action
- Communicate solution
- Update billing if needed

**Step 5: Follow-up**
- Verify consumer satisfaction
- Close complaint
- Generate report
- Update knowledge base""",

        "safety": """🛡️ **Field Safety Procedures**

**Before Leaving Office:**
- Check weather conditions
- Ensure vehicle is roadworthy
- Carry emergency kit
- Inform supervisor of route

**Personal Protective Equipment:**
- Safety helmet (always)
- High-visibility vest
- Safety shoes with grip
- Insulated gloves for electrical work

**Field Safety Rules:**
- Never work alone at night
- Maintain safe distance from live wires
- Use proper ladders and tools
- Report hazardous conditions

**Emergency Procedures:**
- Know location of nearest hospital
- Carry first aid kit
- Have emergency contact numbers
- Report accidents immediately

**Vehicle Safety:**
- Obey traffic rules
- Park safely
- Secure equipment
- Regular vehicle maintenance""",

        "software": """💻 **MDC Software Usage Guide**

**Mobile App Features:**
- Route planning and navigation
- Meter reading data entry
- Photo capture for anomalies
- Real-time data synchronization
- Offline capability

**Daily Workflow:**
1. Login and sync data
2. View assigned routes
3. Navigate to first consumer
4. Enter meter reading
5. Flag any issues
6. Move to next location

**Data Entry Best Practices:**
- Double-check meter numbers
- Enter readings accurately
- Add detailed notes for anomalies
- Take clear photos when needed
- Sync data frequently

**Reporting Features:**
- Daily reading summary
- Anomaly reports
- Consumer feedback
- Performance metrics

**Troubleshooting:**
- Clear app cache if slow
- Restart app for sync issues
- Contact IT support for technical problems
- Backup data regularly"""
    }
    
    topic_key = topic.lower().replace(' ', '')
    if topic_key in guides:
        return guides[topic_key]
    else:
        return f"Guide for '{topic}' not found. Available guides: meter reading, anomaly, complaint, safety, software"

def get_fallback_response(query):
    """Enhanced fallback response with suggestions"""
    return f"""🤔 I specialize in WAPDA meter reading and MDC operations. Your question about "{query}" seems outside my expertise.

**I can help you with:**
• 📊 Meter reading procedures and techniques
• 👨‍💼 MDC responsibilities and daily routines  
• 🏛️ WAPDA organizational structure and operations
• 💰 Billing processes and tariff systems
• ⚡ Meter types, installation, and maintenance
• 👥 Consumer categories and connection requirements
• 🚨 Anomaly detection and investigation
• 📞 Consumer complaint resolution
• 🛡️ Safety procedures and protocols
• 💻 MDC software and tools usage
• 🚀 Career paths in meter reading division

**Try asking:**
- "How does meter reading work?"
- "What are MDC responsibilities?" 
- "Guide meter reading" (for step-by-step tutorials)
- "Quiz" (for interactive assessment)

What WAPDA or MDC topic would you like to know about?"""

@app.route('/')
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image file found in request.'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'message': 'No selected file.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'message': 'Unsupported image type.'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    image_url = f'/uploads/{filename}'
    return jsonify({'success': True, 'message': 'Image uploaded successfully.', 'filename': filename, 'url': image_url})

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message.strip():
        return jsonify({'response': 'Please type a message.'})
    
    # Find relevant answer
    answer = find_relevant_answer(user_message)
    
    if answer:
        bot_response = answer
    else:
        bot_response = f"I'm a specialist chatbot about WAPDA meter reading and MDC (Meter Data Controller) operations. Your question '{user_message}' seems unrelated to my expertise. Please ask me about:\n- Meter reading processes\n- WAPDA operations\n- MDC responsibilities\n- Billing procedures\n- Meter types\n- Consumer categories\n- Any issues related to meter data and WAPDA"
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

