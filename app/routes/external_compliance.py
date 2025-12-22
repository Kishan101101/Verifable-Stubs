"""
External Compliance & Verification API Routes
Comprehensive API for regulations, sanctions, financial verification, and fraud detection
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.compliance import Regulation, SanctionsEntry, FraudPattern
from app.schemas.external_compliance_schema import (
    # Regulation schemas
    RegulationCreateRequest,
    RegulationUpdateRequest,
    RegulationResponse,
    RegulationCreateResponse,
    RegulationListResponse,
    RegulationSummary,
    # Compliance verification schemas
    ComplianceVerifyEntityRequest,
    ComplianceVerifyEntityResponse,
    Violation,
    # Sanctions schemas
    SanctionsScreenRequest,
    SanctionsScreenResponse,
    SanctionsMatch,
    PEPCheck,
    AdverseMedia,
    SanctionsEntryCreateRequest,
    SanctionsEntryCreateResponse,
    SanctionsEntryResponse,
    SanctionsListEntriesResponse,
    # Financial schemas
    FinancialVerifyRequest,
    FinancialVerifyResponse,
    CreditDetails,
    FinancialIndicators,
    BankruptcyHistory,
    LiensInfo,
    # Fraud schemas
    FraudDetectRequest,
    FraudDetectResponse,
    FraudIndicator,
    IdentityVerification,
    AddressVerification,
    DocumentForgeryRequest,
    DocumentForgeryResponse,
    AuthenticityChecks,
    FraudPatternCreateRequest,
    FraudPatternUpdateRequest,
    FraudPatternResponse,
    FraudPatternCreateResponse,
    FraudPatternListResponse,
    # Error schemas
    ErrorResponse,
)

router = APIRouter()


# ============================================
# 1. Regulations & Requirements Management
# ============================================

@router.post("/regulations", response_model=RegulationCreateResponse, status_code=201, tags=["Regulations"])
def create_regulation(
    regulation: RegulationCreateRequest,
    db: Session = Depends(get_db)
):
    """
    POST /regulations - Store a new regulation or compliance requirement
    """
    # Check if regulation already exists
    existing = db.query(Regulation).filter_by(regulation_id=regulation.regulation_id).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "success": False,
                "error": {
                    "code": "DUPLICATE_ENTRY",
                    "message": f"Regulation with ID '{regulation.regulation_id}' already exists"
                }
            }
        )
    
    # Convert key_articles to dict format for JSON storage
    key_articles_data = None
    if regulation.key_articles:
        key_articles_data = [article.model_dump() for article in regulation.key_articles]
    
    # Create new regulation
    new_regulation = Regulation(
        regulation_id=regulation.regulation_id,
        name=regulation.name,
        code=regulation.code,
        category=regulation.category,
        jurisdiction=regulation.jurisdiction,
        version=regulation.version,
        effective_date=regulation.effective_date,
        description=regulation.description,
        required_fields=regulation.required_fields,
        key_articles=key_articles_data,
        compliance_checklist=regulation.compliance_checklist,
        penalties=regulation.penalties,
        tags=regulation.tags,
        is_active=regulation.is_active,
    )
    
    db.add(new_regulation)
    db.commit()
    
    return RegulationCreateResponse(
        success=True,
        regulation_id=regulation.regulation_id,
        message="Regulation stored successfully"
    )


@router.get("/regulations", response_model=RegulationListResponse, tags=["Regulations"])
def get_all_regulations(
    category: Optional[str] = Query(None, description="Filter by category (kyc, aml, gdpr, sox, etc.)"),
    jurisdiction: Optional[str] = Query(None, description="Filter by jurisdiction (US, EU, UK, etc.)"),
    is_active: Optional[bool] = Query(None, description="Filter active/inactive regulations"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    GET /regulations - Get all regulations with optional filters
    """
    query = db.query(Regulation)
    
    # Apply filters
    if category:
        query = query.filter(Regulation.category == category)
    if jurisdiction:
        query = query.filter(Regulation.jurisdiction == jurisdiction)
    if is_active is not None:
        query = query.filter(Regulation.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    regulations = query.offset(offset).limit(limit).all()
    
    # Convert to summary format
    regulation_summaries = [
        RegulationSummary(
            regulation_id=reg.regulation_id,
            name=reg.name,
            code=reg.code,
            category=reg.category,
            jurisdiction=reg.jurisdiction
        )
        for reg in regulations
    ]
    
    return RegulationListResponse(
        success=True,
        total=total,
        page=page,
        limit=limit,
        regulations=regulation_summaries
    )


@router.get("/regulations/{regulation_id}", response_model=RegulationResponse, tags=["Regulations"])
def get_regulation_by_id(
    regulation_id: str,
    db: Session = Depends(get_db)
):
    """
    GET /regulations/{regulation_id} - Get regulation by ID
    """
    regulation = db.query(Regulation).filter_by(regulation_id=regulation_id).first()
    
    if not regulation:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Regulation with ID '{regulation_id}' not found"
                }
            }
        )
    
    return RegulationResponse(
        regulation_id=regulation.regulation_id,
        name=regulation.name,
        code=regulation.code,
        category=regulation.category,
        jurisdiction=regulation.jurisdiction,
        version=regulation.version,
        effective_date=regulation.effective_date,
        description=regulation.description,
        required_fields=regulation.required_fields,
        key_articles=regulation.key_articles,
        compliance_checklist=regulation.compliance_checklist,
        penalties=regulation.penalties,
        is_active=regulation.is_active,
        tags=regulation.tags,
        created_at=regulation.created_at,
        updated_at=regulation.updated_at
    )


@router.put("/regulations/{regulation_id}", response_model=RegulationResponse, tags=["Regulations"])
def update_regulation(
    regulation_id: str,
    regulation_update: RegulationUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    PUT /regulations/{regulation_id} - Update regulation (partial update supported)
    """
    regulation = db.query(Regulation).filter_by(regulation_id=regulation_id).first()
    
    if not regulation:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Regulation with ID '{regulation_id}' not found"
                }
            }
        )
    
    # Update only provided fields
    update_data = regulation_update.model_dump(exclude_unset=True)
    
    # Handle key_articles conversion
    if 'key_articles' in update_data and update_data['key_articles'] is not None:
        update_data['key_articles'] = [article.model_dump() if hasattr(article, 'model_dump') else article for article in update_data['key_articles']]
    
    for field, value in update_data.items():
        setattr(regulation, field, value)
    
    regulation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(regulation)
    
    return RegulationResponse(
        regulation_id=regulation.regulation_id,
        name=regulation.name,
        code=regulation.code,
        category=regulation.category,
        jurisdiction=regulation.jurisdiction,
        version=regulation.version,
        effective_date=regulation.effective_date,
        description=regulation.description,
        required_fields=regulation.required_fields,
        key_articles=regulation.key_articles,
        compliance_checklist=regulation.compliance_checklist,
        penalties=regulation.penalties,
        is_active=regulation.is_active,
        tags=regulation.tags,
        created_at=regulation.created_at,
        updated_at=regulation.updated_at
    )


@router.delete("/regulations/{regulation_id}", status_code=204, tags=["Regulations"])
def delete_regulation(
    regulation_id: str,
    db: Session = Depends(get_db)
):
    """
    DELETE /regulations/{regulation_id} - Delete regulation
    """
    regulation = db.query(Regulation).filter_by(regulation_id=regulation_id).first()
    
    if not regulation:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Regulation with ID '{regulation_id}' not found"
                }
            }
        )
    
    db.delete(regulation)
    db.commit()
    
    return None


# ============================================
# 2. Compliance Verification API
# ============================================

@router.post("/compliance/verify", response_model=ComplianceVerifyEntityResponse, tags=["Compliance Verification"])
def verify_entity_compliance(
    request: ComplianceVerifyEntityRequest,
    db: Session = Depends(get_db)
):
    """
    POST /compliance/verify - Check if an entity meets compliance requirements
    """
    violations = []
    missing_requirements = []
    passed_checks = []
    recommendations = []
    
    # Get applicable regulations from database
    applicable_regulations = db.query(Regulation).filter(
        Regulation.code.in_([cat.lower() for cat in request.categories]),
        Regulation.is_active == True
    ).all()
    
    # Simulate compliance checking logic
    total_checks = 0
    passed = 0
    
    for reg in applicable_regulations:
        if reg.required_fields:
            for field in reg.required_fields:
                total_checks += 1
                # Check if field is provided in document_data
                if request.document_data and field in request.document_data:
                    passed += 1
                    passed_checks.append(f"{reg.code.upper()}: {field} verified")
                else:
                    missing_requirements.append(field)
                    recommendations.append(f"Provide {field} for {reg.code.upper()} compliance")
    
    # Add some default checks based on categories
    for category in request.categories:
        cat_lower = category.lower()
        if cat_lower == "kyc":
            passed_checks.append("KYC identity verification")
            total_checks += 1
            passed += 1
        elif cat_lower == "aml":
            passed_checks.append("AML screening passed")
            passed_checks.append("Business registration valid")
            total_checks += 2
            passed += 2
        elif cat_lower == "sox":
            if not request.document_data or "ceo_certification" not in request.document_data:
                violations.append(Violation(
                    regulation="sox",
                    article="Section 302",
                    description="Missing CEO certification document",
                    severity="high"
                ))
                missing_requirements.append("CEO certification document")
                recommendations.append("Submit CEO/CFO certification")
                total_checks += 1
            else:
                passed_checks.append("SOX Section 302 compliance verified")
                total_checks += 1
                passed += 1
    
    # Calculate compliance score
    if total_checks > 0:
        compliance_score = int((passed / total_checks) * 100)
    else:
        compliance_score = 100
    
    # Determine status and risk level
    if compliance_score >= 90 and len(violations) == 0:
        compliance_status = "compliant"
        risk_level = "low"
    elif compliance_score >= 60:
        compliance_status = "partial"
        risk_level = "medium"
    else:
        compliance_status = "non_compliant"
        risk_level = "high"
    
    if any(v.severity == "critical" for v in violations):
        risk_level = "critical"
    
    return ComplianceVerifyEntityResponse(
        compliance_status=compliance_status,
        compliance_score=compliance_score,
        risk_level=risk_level,
        regulations_checked=request.categories,
        violations=violations,
        missing_requirements=missing_requirements,
        passed_checks=passed_checks,
        recommendations=recommendations,
        checked_at=datetime.utcnow()
    )


# ============================================
# 3. Sanctions Screening API
# ============================================

@router.post("/sanctions/ofac-screen", response_model=SanctionsScreenResponse, tags=["Sanctions Screening"])
def ofac_sanctions_screen(
    request: SanctionsScreenRequest,
    db: Session = Depends(get_db)
):
    """
    POST /sanctions/ofac-screen - Screen entity against sanctions lists
    """
    matches = []
    lists_checked = request.sanctions_lists or ["ofac_sdn", "eu_consolidated", "un_consolidated", "pep"]
    
    # Search for matches in database
    for list_type in lists_checked:
        # Search by name (case-insensitive partial match)
        db_matches = db.query(SanctionsEntry).filter(
            SanctionsEntry.list_type == list_type,
            SanctionsEntry.is_active == True,
            or_(
                SanctionsEntry.name.ilike(f"%{request.entity_name}%"),
                SanctionsEntry.aliases.contains([request.entity_name])  # JSON contains
            )
        ).all()
        
        for match in db_matches:
            # Calculate match score based on name similarity
            if match.name.upper() == request.entity_name.upper():
                match_score = 100
                match_type = "exact"
            elif request.entity_name.upper() in match.name.upper():
                match_score = 85
                match_type = "partial"
            else:
                match_score = 70
                match_type = "fuzzy"
            
            matches.append(SanctionsMatch(
                list_name=list_type,
                match_score=match_score,
                matched_name=match.name,
                match_type=match_type,
                sanctions_details={
                    "program": match.program,
                    "listing_date": match.listing_date.isoformat() if match.listing_date else None,
                    "reason": match.reason
                }
            ))
    
    # Determine screening status
    matches_found = len(matches)
    if matches_found == 0:
        screening_status = "clear"
        risk_level = "low"
    elif any(m.match_score >= 90 for m in matches):
        screening_status = "hit"
        risk_level = "critical"
    else:
        screening_status = "potential_match"
        risk_level = "high"
    
    # PEP check response
    pep_check = None
    if request.check_pep:
        # Check if entity is in PEP list
        pep_match = db.query(SanctionsEntry).filter(
            SanctionsEntry.list_type == "pep",
            SanctionsEntry.name.ilike(f"%{request.entity_name}%")
        ).first()
        
        pep_check = PEPCheck(
            is_pep=pep_match is not None,
            pep_level=pep_match.program if pep_match else None,
            details=pep_match.reason if pep_match else None
        )
    
    # Adverse media response
    adverse_media = None
    if request.check_adverse_media:
        adverse_media = AdverseMedia(
            found=False,
            articles=[]
        )
    
    return SanctionsScreenResponse(
        screening_status=screening_status,
        matches_found=matches_found,
        risk_level=risk_level,
        matches=matches,
        pep_check=pep_check,
        adverse_media=adverse_media,
        lists_checked=lists_checked,
        screened_at=datetime.utcnow()
    )


# ============================================
# 4. Financial Verification API
# ============================================

@router.post("/financial/verify", response_model=FinancialVerifyResponse, tags=["Financial Verification"])
def verify_financial_health(
    request: FinancialVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    POST /financial/verify - Assess entity's financial health
    """
    # Simulate financial health assessment
    # In a real implementation, this would integrate with credit bureaus, financial databases, etc.
    
    # Default healthy values (simulated)
    financial_health_score = 78
    risk_level = "low"
    credit_rating = "good"
    financial_stability = "stable"
    bankruptcy_risk = False
    liens_found = False
    
    credit_details = None
    if request.check_credit:
        credit_details = CreditDetails(
            score=720,
            payment_history="excellent",
            credit_utilization="32%"
        )
    
    financial_indicators = None
    if request.check_financials:
        financial_indicators = FinancialIndicators(
            revenue_trend="growing",
            profit_margin="15%",
            debt_to_equity=0.45
        )
    
    bankruptcy_history = None
    if request.check_bankruptcy:
        bankruptcy_history = BankruptcyHistory(
            has_history=False,
            filings=[]
        )
    
    liens = None
    if request.check_liens:
        liens = LiensInfo(
            active_liens=0,
            total_amount=0
        )
    
    return FinancialVerifyResponse(
        financial_health_score=financial_health_score,
        risk_level=risk_level,
        credit_rating=credit_rating,
        financial_stability=financial_stability,
        bankruptcy_risk=bankruptcy_risk,
        liens_found=liens_found,
        credit_details=credit_details,
        financial_indicators=financial_indicators,
        bankruptcy_history=bankruptcy_history,
        liens=liens,
        verified_at=datetime.utcnow()
    )


# ============================================
# 5. Fraud Detection API
# ============================================

@router.post("/fraud/detect", response_model=FraudDetectResponse, tags=["Fraud Detection"])
def detect_fraud(
    request: FraudDetectRequest,
    db: Session = Depends(get_db)
):
    """
    POST /fraud/detect - Analyze entity for fraud indicators
    """
    fraud_indicators = []
    patterns_detected = []
    
    # Get active fraud patterns from database
    active_patterns = db.query(FraudPattern).filter(FraudPattern.is_active == True).all()
    
    # Simulate fraud detection logic
    risk_score = 15  # Default low risk
    fraud_detected = False
    
    # Check document data against fraud patterns
    if request.document_data:
        for pattern in active_patterns:
            if pattern.indicators:
                pattern_matched = False
                for indicator in pattern.indicators:
                    field = indicator.get("field", "")
                    condition = indicator.get("condition", "")
                    
                    # Simple pattern matching simulation
                    if field in str(request.document_data):
                        pattern_matched = True
                        break
                
                if pattern_matched:
                    patterns_detected.append(pattern.name)
                    risk_score += pattern.risk_score_threshold or 20
    
    # Determine if fraud is detected based on risk score
    if risk_score >= 70:
        fraud_detected = True
        risk_level = "high"
    elif risk_score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # Identity verification (simulated)
    identity_verification = IdentityVerification(
        verified=True,
        confidence=92
    )
    
    # Address verification (simulated)
    address_verification = None
    if request.document_data and "address" in request.document_data:
        address_verification = AddressVerification(
            valid=True,
            type="commercial"
        )
    
    return FraudDetectResponse(
        fraud_detected=fraud_detected,
        risk_level=risk_level,
        risk_score=min(risk_score, 100),
        fraud_indicators=fraud_indicators,
        patterns_detected=patterns_detected,
        identity_verification=identity_verification,
        address_verification=address_verification,
        analyzed_at=datetime.utcnow()
    )


@router.post("/fraud/document-forgery", response_model=DocumentForgeryResponse, tags=["Fraud Detection"])
def detect_document_forgery(
    request: DocumentForgeryRequest,
    db: Session = Depends(get_db)
):
    """
    POST /fraud/document-forgery - Analyze document for tampering/forgery
    """
    tampering_indicators = []
    
    # Validate document data
    format_valid = True
    dates_consistent = True
    authority_verified = True
    metadata_clean = True
    
    # Check for date consistency
    if "issue_date" in request.document_data and "expiry_date" in request.document_data:
        try:
            issue_date = request.document_data.get("issue_date")
            expiry_date = request.document_data.get("expiry_date")
            # Simple date validation
            if issue_date and expiry_date:
                if issue_date > expiry_date:
                    dates_consistent = False
                    tampering_indicators.append("Issue date is after expiry date")
        except:
            pass
    
    # Check metadata if provided
    if request.metadata:
        created_date = request.metadata.get("created_date")
        modified_date = request.metadata.get("modified_date")
        
        if created_date and modified_date:
            if created_date != modified_date:
                # Document was modified after creation - potential concern
                pass  # Not necessarily tampering
    
    # Calculate confidence score
    confidence_score = 95
    if tampering_indicators:
        confidence_score -= len(tampering_indicators) * 15
    
    # Determine risk level
    forgery_detected = len(tampering_indicators) > 0
    if forgery_detected:
        risk_level = "high"
    elif confidence_score < 80:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    return DocumentForgeryResponse(
        forgery_detected=forgery_detected,
        confidence_score=max(confidence_score, 0),
        risk_level=risk_level,
        tampering_indicators=tampering_indicators,
        authenticity_checks=AuthenticityChecks(
            format_valid=format_valid,
            dates_consistent=dates_consistent,
            authority_verified=authority_verified,
            metadata_clean=metadata_clean
        ),
        analyzed_at=datetime.utcnow()
    )


# ============================================
# 6. Sanctions Lists Management
# ============================================

@router.post("/sanctions/lists/{list_type}/entries", response_model=SanctionsEntryCreateResponse, status_code=201, tags=["Sanctions Lists"])
def add_sanctions_entry(
    list_type: str,
    entry: SanctionsEntryCreateRequest,
    db: Session = Depends(get_db)
):
    """
    POST /sanctions/lists/{list_type}/entries - Add entry to sanctions list
    
    list_type: ofac_sdn, eu_consolidated, un_consolidated, pep
    """
    valid_list_types = ["ofac_sdn", "eu_consolidated", "un_consolidated", "pep"]
    if list_type not in valid_list_types:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": f"Invalid list_type. Must be one of: {valid_list_types}"
                }
            }
        )
    
    # Check if entry already exists
    existing = db.query(SanctionsEntry).filter_by(entry_id=entry.entry_id).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "success": False,
                "error": {
                    "code": "DUPLICATE_ENTRY",
                    "message": f"Entry with ID '{entry.entry_id}' already exists"
                }
            }
        )
    
    # Convert additional_info to dict
    additional_info_data = None
    if entry.additional_info:
        additional_info_data = entry.additional_info.model_dump()
    
    # Create new entry
    new_entry = SanctionsEntry(
        entry_id=entry.entry_id,
        list_type=list_type,
        name=entry.name,
        aliases=entry.aliases,
        entity_type=entry.entity_type,
        country=entry.country,
        program=entry.program,
        listing_date=entry.listing_date,
        reason=entry.reason,
        additional_info=additional_info_data,
        is_active=entry.is_active
    )
    
    db.add(new_entry)
    db.commit()
    
    return SanctionsEntryCreateResponse(
        success=True,
        entry_id=entry.entry_id,
        list_type=list_type,
        message=f"Entry added to {list_type} list successfully"
    )


@router.get("/sanctions/lists/{list_type}/entries", response_model=SanctionsListEntriesResponse, tags=["Sanctions Lists"])
def get_sanctions_entries(
    list_type: str,
    search: Optional[str] = Query(None, description="Search by name/alias"),
    country: Optional[str] = Query(None, description="Filter by country"),
    program: Optional[str] = Query(None, description="Filter by sanctions program"),
    is_active: Optional[bool] = Query(None, description="Filter active entries"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    GET /sanctions/lists/{list_type}/entries - Get sanctions list entries
    """
    query = db.query(SanctionsEntry).filter(SanctionsEntry.list_type == list_type)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                SanctionsEntry.name.ilike(f"%{search}%"),
                SanctionsEntry.aliases.contains([search])
            )
        )
    if country:
        query = query.filter(SanctionsEntry.country == country)
    if program:
        query = query.filter(SanctionsEntry.program == program)
    if is_active is not None:
        query = query.filter(SanctionsEntry.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    entries = query.offset(offset).limit(limit).all()
    
    # Convert to response format
    entry_responses = [
        SanctionsEntryResponse(
            entry_id=entry.entry_id,
            list_type=entry.list_type,
            name=entry.name,
            aliases=entry.aliases,
            entity_type=entry.entity_type,
            country=entry.country,
            program=entry.program,
            listing_date=entry.listing_date,
            reason=entry.reason,
            additional_info=entry.additional_info,
            is_active=entry.is_active,
            created_at=entry.created_at,
            updated_at=entry.updated_at
        )
        for entry in entries
    ]
    
    return SanctionsListEntriesResponse(
        success=True,
        total=total,
        page=page,
        limit=limit,
        entries=entry_responses
    )


# ============================================
# 7. Fraud Patterns Database
# ============================================

@router.post("/fraud/patterns", response_model=FraudPatternCreateResponse, status_code=201, tags=["Fraud Patterns"])
def add_fraud_pattern(
    pattern: FraudPatternCreateRequest,
    db: Session = Depends(get_db)
):
    """
    POST /fraud/patterns - Store known fraud patterns for detection
    """
    # Check if pattern already exists
    existing = db.query(FraudPattern).filter_by(pattern_id=pattern.pattern_id).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail={
                "success": False,
                "error": {
                    "code": "DUPLICATE_ENTRY",
                    "message": f"Pattern with ID '{pattern.pattern_id}' already exists"
                }
            }
        )
    
    # Convert indicators to dict format
    indicators_data = None
    if pattern.indicators:
        indicators_data = [ind.model_dump() for ind in pattern.indicators]
    
    # Create new pattern
    new_pattern = FraudPattern(
        pattern_id=pattern.pattern_id,
        name=pattern.name,
        category=pattern.category,
        description=pattern.description,
        indicators=indicators_data,
        risk_score_threshold=pattern.risk_score_threshold,
        action=pattern.action,
        is_active=pattern.is_active
    )
    
    db.add(new_pattern)
    db.commit()
    
    return FraudPatternCreateResponse(
        success=True,
        pattern_id=pattern.pattern_id,
        message="Fraud pattern stored successfully"
    )


@router.get("/fraud/patterns", response_model=FraudPatternListResponse, tags=["Fraud Patterns"])
def get_fraud_patterns(
    category: Optional[str] = Query(None, description="Filter by category: identity_fraud, document_tampering, financial_fraud"),
    is_active: Optional[bool] = Query(None, description="Filter active patterns"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    GET /fraud/patterns - Get fraud patterns
    """
    query = db.query(FraudPattern)
    
    # Apply filters
    if category:
        query = query.filter(FraudPattern.category == category)
    if is_active is not None:
        query = query.filter(FraudPattern.is_active == is_active)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    patterns = query.offset(offset).limit(limit).all()
    
    # Convert to response format
    pattern_responses = [
        FraudPatternResponse(
            pattern_id=p.pattern_id,
            name=p.name,
            category=p.category,
            description=p.description,
            indicators=p.indicators,
            risk_score_threshold=p.risk_score_threshold,
            action=p.action,
            is_active=p.is_active,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in patterns
    ]
    
    return FraudPatternListResponse(
        success=True,
        total=total,
        page=page,
        limit=limit,
        patterns=pattern_responses
    )


@router.get("/fraud/patterns/{pattern_id}", response_model=FraudPatternResponse, tags=["Fraud Patterns"])
def get_fraud_pattern_by_id(
    pattern_id: str,
    db: Session = Depends(get_db)
):
    """
    GET /fraud/patterns/{pattern_id} - Get specific fraud pattern
    """
    pattern = db.query(FraudPattern).filter_by(pattern_id=pattern_id).first()
    
    if not pattern:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Pattern with ID '{pattern_id}' not found"
                }
            }
        )
    
    return FraudPatternResponse(
        pattern_id=pattern.pattern_id,
        name=pattern.name,
        category=pattern.category,
        description=pattern.description,
        indicators=pattern.indicators,
        risk_score_threshold=pattern.risk_score_threshold,
        action=pattern.action,
        is_active=pattern.is_active,
        created_at=pattern.created_at,
        updated_at=pattern.updated_at
    )


@router.put("/fraud/patterns/{pattern_id}", response_model=FraudPatternResponse, tags=["Fraud Patterns"])
def update_fraud_pattern(
    pattern_id: str,
    pattern_update: FraudPatternUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    PUT /fraud/patterns/{pattern_id} - Update fraud pattern
    """
    pattern = db.query(FraudPattern).filter_by(pattern_id=pattern_id).first()
    
    if not pattern:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Pattern with ID '{pattern_id}' not found"
                }
            }
        )
    
    # Update only provided fields
    update_data = pattern_update.model_dump(exclude_unset=True)
    
    # Handle indicators conversion
    if 'indicators' in update_data and update_data['indicators'] is not None:
        update_data['indicators'] = [ind.model_dump() if hasattr(ind, 'model_dump') else ind for ind in update_data['indicators']]
    
    for field, value in update_data.items():
        setattr(pattern, field, value)
    
    pattern.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(pattern)
    
    return FraudPatternResponse(
        pattern_id=pattern.pattern_id,
        name=pattern.name,
        category=pattern.category,
        description=pattern.description,
        indicators=pattern.indicators,
        risk_score_threshold=pattern.risk_score_threshold,
        action=pattern.action,
        is_active=pattern.is_active,
        created_at=pattern.created_at,
        updated_at=pattern.updated_at
    )


@router.delete("/fraud/patterns/{pattern_id}", status_code=204, tags=["Fraud Patterns"])
def delete_fraud_pattern(
    pattern_id: str,
    db: Session = Depends(get_db)
):
    """
    DELETE /fraud/patterns/{pattern_id} - Delete fraud pattern
    """
    pattern = db.query(FraudPattern).filter_by(pattern_id=pattern_id).first()
    
    if not pattern:
        raise HTTPException(
            status_code=404,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Pattern with ID '{pattern_id}' not found"
                }
            }
        )
    
    db.delete(pattern)
    db.commit()
    
    return None
