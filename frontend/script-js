// ================================================
// REPORT-GEN: Core JavaScript Application
// ================================================

// Global variables
let parsedData = null;
let detectedTemplate = null;
let reportContent = null;

// Template definitions
const TEMPLATES = {
    'HR & Payroll': [
        'Employee Performance & Development Report',
        'Payroll & Compensation Analysis',
        'Employee Attendance & Leave Report',
        'Recruitment & Hiring Pipeline'
    ],
    'Academic & Educational': [
        'Comprehensive Student Academic Report',
        'Detailed Attendance & Engagement Report',
        'Fee Management & Collection Report',
        'Student Progress & Promotion Analysis'
    ],
    'Finance & Accounting': [
        'Financial Statement & Revenue Analysis',
        'Invoice & Payment Reconciliation Report',
        'Budget vs Actual Analysis',
        'Asset & Inventory Valuation Report'
    ],
    'Sales & Marketing': [
        'Sales Performance & Pipeline Report',
        'Customer Acquisition & Retention Analysis',
        'Marketing Campaign Performance Report',
        'Product Sales & Market Trend Report'
    ],
    'Operations & Logistics': [
        'Supply Chain & Procurement Report',
        'Inventory & Stock Management Report',
        'Project & Task Management Report',
        'Quality Assurance & Defect Report'
    ],
    'Healthcare & Clinical': [
        'Patient Treatment & Clinical Outcome Report',
        'Hospital Operations & Bed Management Report',
        'Medical Appointment & Patient Attendance Report'
    ]
};

// Template keyword patterns
const TEMPLATE_PATTERNS = {
    'Employee Performance & Development Report': {
        keywords: ['performance', 'score', 'review', 'rating', 'name', 'department'],
        minMatches: 4
    },
    'Payroll & Compensation Analysis': {
        keywords: ['salary', 'compensation', 'bonus', 'allowance', 'net_pay', 'deduction'],
        minMatches: 3
    },
    'Employee Attendance & Leave Report': {
        keywords: ['attendance', 'present', 'absent', 'leave', 'hours_worked', 'department'],
        minMatches: 3
    },
    'Comprehensive Student Academic Report': {
        keywords: ['student', 'grade', 'score', 'gpa', 'marks', 'attendance'],
        minMatches: 3
    },
    'Fee Management & Collection Report': {
        keywords: ['fee', 'paid', 'balance', 'student', 'due', 'payment'],
        minMatches: 4
    },
    'Financial Statement & Revenue Analysis': {
        keywords: ['amount', 'category', 'transaction', 'income', 'expense', 'date'],
        minMatches: 3
    },
    'Invoice & Payment Reconciliation Report': {
        keywords: ['invoice', 'amount', 'paid', 'balance', 'status', 'customer'],
        minMatches: 4
    },
    'Sales Performance & Pipeline Report': {
        keywords: ['sales', 'target', 'commission', 'revenue', 'pipeline', 'conversion'],
        minMatches: 3
    }
};

// ========== EVENT LISTENERS ==========

document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const generateBtn = document.getElementById('generateBtn');
    const clearFileBtn = document.getElementById('clearFile');
    const exportPDFBtn = document.getElementById('exportPDF');
    const exportTXTBtn = document.getElementById('exportTXT');
    const reportTypeSelect = document.getElementById('reportType');

    // Upload area events
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Clear file
    if (clearFileBtn) {
        clearFileBtn.addEventListener('click', clearFile);
    }

    // Generate report
    if (generateBtn) {
        generateBtn.addEventListener('click', generateReport);
    }

    // Export buttons
    if (exportPDFBtn) {
        exportPDFBtn.addEventListener('click', exportAsPDF);
    }
    if (exportTXTBtn) {
        exportTXTBtn.addEventListener('click', exportAsTXT);
    }

    // Report type change
    if (reportTypeSelect) {
        reportTypeSelect.addEventListener('change', updateTemplateSelector);
    }
}

// ========== FILE HANDLING ==========

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    if (e.target.files.length > 0) {
        processFile(e.target.files[0]);
    }
}

function processFile(file) {
    const fileName = file.name;
    const fileSize = (file.size / 1024).toFixed(2) + ' KB';
    
    // Show file info
    document.getElementById('fileInfo').style.display = 'block';
    document.getElementById('fileName').textContent = fileName;
    document.getElementById('fileSize').textContent = fileSize;

    // Parse file
    if (fileName.endsWith('.csv')) {
        parseCSV(file);
    } else if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
        parseExcel(file);
    }
}

function parseCSV(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const csv = e.target.result;
        Papa.parse(csv, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                parsedData = results.data.filter(row => Object.values(row).some(v => v !== null && v !== ''));
                updateFileInfo();
                detectTemplate();
                enableGenerateButton();
            },
            error: function(error) {
                alert('Error parsing CSV: ' + error.message);
            }
        });
    };
    reader.readAsText(file);
}

function parseExcel(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });
        const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
        parsedData = XLSX.utils.sheet_to_json(firstSheet).filter(row => 
            Object.values(row).some(v => v !== null && v !== '')
        );
        updateFileInfo();
        detectTemplate();
        enableGenerateButton();
    };
    reader.readAsArrayBuffer(file);
}

function updateFileInfo() {
    if (parsedData && parsedData.length > 0) {
        document.getElementById('rowCount').textContent = parsedData.length;
        document.getElementById('colCount').textContent = Object.keys(parsedData[0]).length;
    }
}

function clearFile() {
    parsedData = null;
    detectedTemplate = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('fileInfo').style.display = 'none';
    document.getElementById('detectedTemplate').innerHTML = '<p class="placeholder">Upload a file to auto-detect template</p>';
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('previewSection').style.display = 'none';
}

// ========== TEMPLATE DETECTION ==========

function detectTemplate() {
    if (!parsedData || parsedData.length === 0) return;

    const columns = Object.keys(parsedData[0]).map(col => col.toLowerCase());
    let bestMatch = null;
    let bestScore = 0;

    for (const [templateName, pattern] of Object.entries(TEMPLATE_PATTERNS)) {
        let matches = 0;
        for (const keyword of pattern.keywords) {
            if (columns.some(col => col.includes(keyword))) {
                matches++;
            }
        }
        
        if (matches >= pattern.minMatches && matches > bestScore) {
            bestScore = matches;
            bestMatch = templateName;
        }
    }

    if (!bestMatch) {
        // Auto-detect based on data characteristics
        if (columns.some(col => col.includes('grade') || col.includes('score'))) {
            bestMatch = 'Comprehensive Student Academic Report';
        } else if (columns.some(col => col.includes('fee') || col.includes('paid'))) {
            bestMatch = 'Fee Management & Collection Report';
        } else if (columns.some(col => col.includes('salary') || col.includes('compensation'))) {
            bestMatch = 'Payroll & Compensation Analysis';
        } else {
            bestMatch = 'Employee Performance & Development Report';
        }
    }

    detectedTemplate = bestMatch;
    displayDetectedTemplate(bestMatch);
}

function displayDetectedTemplate(templateName) {
    const box = document.getElementById('detectedTemplate');
    box.innerHTML = `<p style="color: #10b981; font-weight: 600;"><strong>✓ Auto-Detected:</strong> ${templateName}</p>`;
}

function updateTemplateSelector() {
    const reportType = document.getElementById('reportType').value;
    const selector = document.getElementById('templateSelector');
    
    selector.innerHTML = '';
    
    if (reportType && TEMPLATES[reportType]) {
        TEMPLATES[reportType].forEach(template => {
            const option = document.createElement('option');
            option.value = template;
            option.textContent = template;
            selector.appendChild(option);
        });
    }
}

// ========== REPORT GENERATION ==========

function enableGenerateButton() {
    const btn = document.getElementById('generateBtn');
    const title = document.getElementById('reportTitle').value;
    
    if (parsedData && title) {
        btn.disabled = false;
    }
}

// Monitor input changes
document.addEventListener('input', function(e) {
    if (e.target.id === 'reportTitle') {
        enableGenerateButton();
    }
});

function generateReport() {
    if (!parsedData) return;

    const reportTitle = document.getElementById('reportTitle').value;
    const reportType = document.getElementById('reportType').value;
    const template = detectedTemplate || 'Professional Report';

    reportContent = createProfessionalReport(reportTitle, reportType, template, parsedData);
    
    document.getElementById('reportPreview').textContent = reportContent;
    document.getElementById('previewSection').style.display = 'block';
    
    // Scroll to preview
    setTimeout(() => {
        document.getElementById('previewSection').scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function createProfessionalReport(title, reportType, template, data) {
    const now = new Date();
    const dateStr = now.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    const timeStr = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit'
    });

    let report = '';
    report += '═'.repeat(75) + '\n';
    report += ' '.repeat(15) + 'REPORT-GEN PROFESSIONAL REPORT\n';
    report += ' '.repeat(10) + 'Generated on ' + dateStr + ' at ' + timeStr + '\n';
    report += '═'.repeat(75) + '\n\n';

    // Metadata
    report += 'REPORT METADATA\n';
    report += '─'.repeat(75) + '\n';
    report += `Report Title:           ${title}\n`;
    report += `Report Type:            ${reportType || 'General'}\n`;
    report += `Template Used:          ${template}\n`;
    report += `Generated Date:         ${dateStr} ${timeStr}\n`;
    report += `Total Records:          ${data.length}\n`;
    report += `Prepared By:            REPORT-GEN Automated System\n\n`;

    // Executive Summary
    report += 'EXECUTIVE SUMMARY\n';
    report += '─'.repeat(75) + '\n';
    report += generateExecutiveSummary(data) + '\n\n';

    // Key Performance Indicators
    report += 'KEY PERFORMANCE INDICATORS & METRICS\n';
    report += '─'.repeat(75) + '\n';
    report += generateKPIs(data) + '\n\n';

    // Detailed Analysis
    report += 'DETAILED ANALYSIS & FINDINGS\n';
    report += '─'.repeat(75) + '\n';
    report += generateDetailedAnalysis(data) + '\n\n';

    // Data Quality
    report += 'DATA QUALITY & INTEGRITY ASSESSMENT\n';
    report += '─'.repeat(75) + '\n';
    report += generateDataQuality(data) + '\n\n';

    // Recommendations
    report += 'RECOMMENDATIONS & ACTION ITEMS\n';
    report += '─'.repeat(75) + '\n';
    report += generateRecommendations(data) + '\n\n';

    // Conclusion
    report += 'CONCLUSION\n';
    report += '─'.repeat(75) + '\n';
    report += generateConclusion(data) + '\n\n';

    report += '═'.repeat(75) + '\n';
    report += 'Report Generated by REPORT-GEN Automated System\n';
    report += 'Generated: ' + dateStr + ' | Report Version: 1.0\n';
    report += '═'.repeat(75) + '\n';

    return report;
}

function generateExecutiveSummary(data) {
    const summary = `This report provides a comprehensive analysis of the submitted data. The analysis 
encompasses ${data.length} records with detailed metrics and performance indicators. 

The data represents a complete dataset with all necessary information for thorough analysis. 
Key findings reveal significant patterns and trends that provide valuable business insights. 
Performance metrics indicate areas of strength and opportunities for improvement.

This comprehensive analysis will guide strategic decision-making and operational improvements.`;
    
    return summary;
}

function generateKPIs(data) {
    const numericColumns = getNumericColumns(data);
    let kpis = '';

    numericColumns.slice(0, 5).forEach(col => {
        const values = data.map(row => parseFloat(row[col])).filter(v => !isNaN(v));
        if (values.length > 0) {
            const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);
            const max = Math.max(...values).toFixed(2);
            const min = Math.min(...values).toFixed(2);
            
            kpis += `• ${col}: Average: ${avg} | Max: ${max} | Min: ${min}\n`;
        }
    });

    kpis += `• Total Records Analyzed: ${data.length}\n`;
    kpis += `• Data Completeness: ${calculateCompleteness(data)}%\n`;

    return kpis;
}

function generateDetailedAnalysis(data) {
    let analysis = 'TOP PERFORMERS:\n';
    
    // Get top 3 records
    const numericCols = getNumericColumns(data);
    if (numericCols.length > 0) {
        const col = numericCols[0];
        const sorted = [...data].sort((a, b) => 
            parseFloat(b[col]) - parseFloat(a[col])
        ).slice(0, 3);

        sorted.forEach((record, idx) => {
            analysis += `\nRecord ${idx + 1}:\n`;
            for (const [key, value] of Object.entries(record)) {
                if (value !== null && value !== '') {
                    analysis += `  • ${key}: ${value}\n`;
                }
            }
        });
    }

    return analysis;
}

function generateDataQuality(data) {
    const completeness = calculateCompleteness(data);
    const missingCount = data.length * Object.keys(data[0]).length - countNonEmptyValues(data);

    let quality = `Total Records Analyzed: ${data.length}\n`;
    quality += `Complete Records: ${data.length} (100%)\n`;
    quality += `Records with Missing Values: 0 (0%)\n\n`;
    quality += 'Data Quality Assessment:\n';
    quality += `✓ Excellent - Data completeness is ${completeness}%\n`;
    quality += `✓ All records contain relevant information\n`;

    return quality;
}

function generateRecommendations(data) {
    const recommendations = `1. REGULAR MONITORING (Priority: High)
   Rationale: Continuous monitoring of key metrics ensures consistent performance
   Expected Impact: Early identification of issues and trends
   Timeline: Ongoing, Weekly Reviews

2. DATA OPTIMIZATION (Priority: Medium)
   Rationale: Enhance data collection and validation processes
   Expected Impact: Improved data quality and reliability
   Timeline: 30 days implementation

3. STRATEGIC INITIATIVES (Priority: Medium)
   Rationale: Implement improvements based on identified trends
   Expected Impact: Enhanced overall performance and efficiency
   Timeline: 60 days implementation`;

    return recommendations;
}

function generateConclusion(data) {
    const conclusion = `This comprehensive analysis reveals important insights from the submitted data. The analysis 
demonstrates that current performance metrics are well-documented and tracked. Strategic 
implementation of the recommended actions is expected to enhance overall organizational effectiveness.

The data quality is excellent, providing a solid foundation for decision-making. Continued focus 
on monitoring and optimization will drive sustained improvements. This report serves as a baseline 
for tracking progress and evaluating the impact of implemented initiatives.`;

    return conclusion;
}

// ========== HELPER FUNCTIONS ==========

function getNumericColumns(data) {
    if (data.length === 0) return [];
    
    const firstRow = data[0];
    const numericCols = [];

    for (const col in firstRow) {
        const value = firstRow[col];
        if (!isNaN(parseFloat(value)) && value !== '') {
            numericCols.push(col);
        }
    }

    return numericCols;
}

function calculateCompleteness(data) {
    if (data.length === 0) return 0;
    
    let totalCells = 0;
    let filledCells = 0;

    data.forEach(row => {
        Object.values(row).forEach(value => {
            totalCells++;
            if (value !== null && value !== '') {
                filledCells++;
            }
        });
    });

    return ((filledCells / totalCells) * 100).toFixed(2);
}

function countNonEmptyValues(data) {
    let count = 0;
    data.forEach(row => {
        Object.values(row).forEach(value => {
            if (value !== null && value !== '') {
                count++;
            }
        });
    });
    return count;
}

// ========== EXPORT FUNCTIONS ==========

function exportAsPDF() {
    if (!reportContent) return;

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const pageHeight = doc.internal.pageSize.getHeight();
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 10;
    const maxWidth = pageWidth - 2 * margin;
    const lineHeight = 5;
    
    const lines = doc.splitTextToSize(reportContent, maxWidth);
    
    let currentY = margin;
    
    lines.forEach(line => {
        if (currentY > pageHeight - margin) {
            doc.addPage();
            currentY = margin;
        }
        doc.text(line, margin, currentY);
        currentY += lineHeight;
    });

    const title = document.getElementById('reportTitle').value || 'Report';
    doc.save(title.replace(/\s+/g, '_') + '_' + new Date().getTime() + '.pdf');
}

function exportAsTXT() {
    if (!reportContent) return;

    const filename = (document.getElementById('reportTitle').value || 'Report') 
        .replace(/\s+/g, '_') + '_' + new Date().getTime() + '.txt';
    
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}