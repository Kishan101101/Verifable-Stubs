# External Compliance & Verification API Documentation

This API provides a comprehensive suite of tools for regulatory compliance, sanctions screening, financial verification, and fraud detection.

## Base URL
`http://localhost:8001/api`

## 1. Regulations Management
Manage and retrieve regulatory requirements for various jurisdictions and industries.

### List Regulations
`GET /regulations`
- **Query Parameters**:
  - `page` (int): Page number (default: 1)
  - `limit` (int): Items per page (default: 20)
  - `category` (string): Filter by category (e.g., "Data Privacy")
  - `jurisdiction` (string): Filter by jurisdiction (e.g., "US", "EU")
  - `is_active` (boolean): Filter by active status
- **Response**: `RegulationListResponse`

### Get Regulation Details
`GET /regulations/{regulation_id}`
- **Path Parameters**: `regulation_id` (e.g., "REG-GDPR-001")
- **Response**: `RegulationResponse`

### Create Regulation
`POST /regulations`
- **Body**: `RegulationCreateRequest`
- **Response**: `RegulationCreateResponse`

---

## 2. Compliance Verification
Verify entities against specific regulatory frameworks.

### Verify Entity
`POST /compliance/verify`
- **Description**: Checks an entity (individual or company) against specified regulation categories.
- **Body**:
```json
{
  "entity_name": "Acme Corp",
  "entity_type": "company",
  "entity_country": "US",
  "categories": ["kyc", "aml"],
  "document_data": {
    "tax_id": "12-3456789",
    "incorporation_date": "2010-01-01"
  }
}
```
- **Response**: `ComplianceVerifyEntityResponse`

---

## 3. Sanctions Screening
Screen entities against global watchlists and PEP databases.

### OFAC/Sanctions Screening
`POST /sanctions/ofac-screen`
- **Description**: Performs real-time screening against OFAC SDN, EU, UN, and PEP lists.
- **Body**:
```json
{
  "entity_name": "AL-QAEDA",
  "entity_type": "organization",
  "check_pep": true,
  "check_adverse_media": true
}
```
- **Response**: `SanctionsScreenResponse`

---

## 4. Financial Verification
Verify financial stability and risk factors.

### Financial Health Check
`POST /financial/verify`
- **Description**: Analyzes credit scores, bankruptcy history, and active liens.
- **Body**:
```json
{
  "entity_name": "John Doe",
  "entity_country": "US",
  "check_credit": true,
  "check_bankruptcy": true
}
```
- **Response**: `FinancialVerifyResponse`

---

## 5. Fraud Detection
Advanced pattern matching and document analysis for fraud prevention.

### Detect Fraud Patterns
`POST /fraud/detect`
- **Description**: Analyzes entity data against known fraud patterns (Identity theft, Synthetic ID, etc.).
- **Body**:
```json
{
  "entity_name": "John Smith",
  "entity_type": "individual",
  "document_data": {
    "address": "123 Virtual Way",
    "ssn_last_four": "9999"
  }
}
```
- **Response**: `FraudDetectResponse`

### Document Forgery Analysis
`POST /fraud/document-forgery`
- **Description**: Analyzes document metadata and content for signs of tampering or forgery.
- **Body**:
```json
{
  "document_type": "passport",
  "document_data": {
    "mrz_code": "P<USA...",
    "issue_date": "2020-01-01"
  }
}
```
- **Response**: `DocumentForgeryResponse`

---

## Data Models (Schemas)

### Regulation Schema
| Field | Type | Description |
|-------|------|-------------|
| `regulation_id` | string | Unique identifier |
| `name` | string | Full name of regulation |
| `code` | string | Short code (e.g., "gdpr") |
| `jurisdiction` | string | Country or region |
| `is_active` | boolean | Status of the regulation |

### Fraud Pattern Schema
| Field | Type | Description |
|-------|------|-------------|
| `pattern_id` | string | Unique identifier |
| `name` | string | Name of the fraud pattern |
| `risk_score_threshold` | integer | Score that triggers an alert |
| `indicators` | list | List of fields and conditions to check |

---

## Error Handling
The API uses standard HTTP status codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (Invalid input)
- `404`: Not Found
- `422`: Validation Error (Schema mismatch)
- `500`: Internal Server Error
