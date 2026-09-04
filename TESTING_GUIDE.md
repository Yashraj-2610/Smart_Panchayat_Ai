# Testing Guide - Smart Panchayat AI System

## Manual Testing Checklist

### 1. Backend API Testing (using Swagger UI)

**Access:** http://localhost:8000/docs

#### Family Head Portal APIs

- [ ] **POST /api/v1/household/register**
  - Register a new household
  - Verify unique Household ID is generated
  - Check that ward population increments

- [ ] **POST /api/v1/household/{id}/members**
  - Add family members
  - Verify auto-increment of household total_members
  - Check ward population auto-calculation

- [ ] **POST /api/v1/household/{id}/issues**
  - Report village issues
  - Verify issue ID generation
  - Check priority assignment logic

#### Sarpanch Portal APIs

- [ ] **GET /api/v1/sarpanch/dashboard/overview**
  - Verify all population statistics are accurate
  - Check issue counts by category
  - Validate ward summaries

- [ ] **GET /api/v1/sarpanch/analytics/population**
  - Confirm literacy rate calculation
  - Verify employment rate
  - Check demographic breakdowns

- [ ] **POST /api/v1/sarpanch/ai/analyze**
  - Run multi-agent analysis
  - Verify each agent returns findings
  - Check priority scoring logic

- [ ] **POST /api/v1/sarpanch/ai/recommendations/generate**
  - Generate AI recommendations
  - Verify RAG scheme matching
  - Check explainability evidence

#### Government Schemes RAG

- [ ] **GET /api/v1/schemes/search?query=water**
  - Test keyword matching
  - Verify relevant schemes returned
  - Check multilingual scheme names

#### Multilingual

- [ ] **GET /api/v1/i18n/translate/welcome?lang=mr**
  - Test English, Hindi, Marathi translations
  - Verify correct language response

---

### 2. Frontend Testing

#### Family Head Portal (http://localhost:8501)

- [ ] **Language Selection**
  - Switch between English, Hindi, Marathi
  - Verify all labels translate correctly

- [ ] **Household Registration Tab**
  - Fill complete household form
  - Submit and verify success message
  - Note the Household ID for next steps

- [ ] **Add Family Member Tab**
  - Use Household ID from registration
  - Add 3-4 family members with different ages
  - Verify success messages

- [ ] **Report Issue Tab**
  - Submit water, health, education issues
  - Verify issue ID is returned
  - Check multilingual issue submission

#### Sarpanch Dashboard (http://localhost:8502)

- [ ] **Overview Dashboard**
  - Verify population metrics display
  - Check gender distribution pie chart
  - Validate issues by category chart

- [ ] **Population & Demographics**
  - Check literacy and employment rates
  - Verify BPL/APL/Antodaya breakdown

- [ ] **Ward Analytics**
  - Verify ward-wise population table
  - Check ward comparison charts

- [ ] **AI Decision Support**
  - Click "Run Multi-Agent Analysis"
  - Verify all 5+ agents return results
  - Check severity indicators (🟢🟡🔴🚨)
  - Expand agent findings and verify evidence
  - Click "Generate AI Recommendations"
  - Verify priority scores and explanations

- [ ] **Government Schemes**
  - Search for "water pipeline"
  - Verify Jal Jeevan Mission appears
  - Check scheme details and eligibility

- [ ] **Panchayat Reports**
  - Generate report
  - Download JSON summary
  - Verify all data is included

---

### 3. Multi-Agent System Testing

Run the multi-agent analysis and verify each agent's logic:

**Population Agent:**
- Should detect low registration coverage if population < expected
- Should flag ward imbalances

**Water Agent:**
- Should detect high severity if >30% households report water issues
- Should flag critical issues with high affected counts

**Health Agent:**
- Should calculate health issue prevalence rate
- Should correlate sanitation issues with health risks

**Education Agent:**
- Should calculate school-age children vs enrolled students
- Should flag dropout/non-enrollment rates

**Infrastructure Agent:**
- Should aggregate road and electricity issues
- Should prioritize based on affected count

**Priority Agent:**
- Should correctly score issues using formula: `severity_weight × domain_multiplier × affected_multiplier`
- Should rank domains from highest to lowest priority

---

### 4. Data Integrity Testing

- [ ] **Auto-calculation Verification**
  - Add 5 members to a household
  - Check household.total_members = 5
  - Check ward.population increments by 5

- [ ] **Duplicate Prevention**
  - Try adding member with duplicate Aadhar number
  - Verify error is thrown

- [ ] **Data Validation**
  - Try invalid phone number format
  - Try age < 0 or > 120
  - Verify validation errors

---

### 5. RAG Knowledge Base Testing

Test scheme retrieval with different queries:

| Query | Expected Scheme Match |
|-------|----------------------|
| "drinking water pipeline" | Jal Jeevan Mission |
| "toilet construction" | Swachh Bharat Mission |
| "farmer subsidy" | PM-KISAN |
| "road repair" | PMGSY |
| "school dropout" | Samagra Shiksha |
| "health insurance" | Ayushman Bharat |

---

### 6. Multilingual Testing

Test UI in all 3 languages:

| Screen | English | Hindi | Marathi |
|--------|---------|-------|---------|
| Welcome | "Welcome to Smart Panchayat System" | "स्मार्ट पंचायत प्रणाली में आपका स्वागत है" | "स्मार्ट पंचायत प्रणालीमध्ये आपले स्वागत आहे" |
| Household Registration | "Household Registration" | "घर का पंजीकरण" | "घर नोंदणी" |

---

## Automated Testing (Future Enhancement)

### Unit Tests (pytest)

```python
# tests/test_household_service.py
def test_create_household():
    # Test household creation logic
    pass

def test_add_member_increments_population():
    # Verify auto-calculation
    pass
```

### Integration Tests

```python
# tests/test_api_endpoints.py
def test_household_registration_endpoint():
    response = client.post("/api/v1/household/register", json={...})
    assert response.status_code == 201
```

---

## Performance Testing

- [ ] Test with 100+ households
- [ ] Test with 500+ family members
- [ ] Test multi-agent analysis with large dataset
- [ ] Measure API response times

---

## Expected Results

✅ **All API endpoints return 200/201 status codes**  
✅ **Database auto-calculations are accurate**  
✅ **Multi-agent system produces explainable recommendations**  
✅ **RAG retrieves relevant government schemes**  
✅ **Multilingual labels render correctly**  
✅ **Charts and visualizations display properly**

---

## Bug Reporting

If you find issues:
1. Note the exact steps to reproduce
2. Capture error messages/logs
3. Check browser console (F12) for frontend errors
4. Review backend terminal for API errors

---

## Demo Data Verification

After running `seed_demo_data.py`:

```bash
# Expected counts:
Total Wards: 6
Total Households: 29
Total Family Members: 100+
Total Issues: 10
Total AI Recommendations: 10
```
