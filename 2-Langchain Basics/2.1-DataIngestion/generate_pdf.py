from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os

def create_pdf():
    # Create the PDF document
    doc = SimpleDocTemplate("sample_document.pdf", pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2E86AB'),
        alignment=1  # Center alignment
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        textColor=HexColor('#A23B72'),
        alignment=0  # Left alignment
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leading=16,
        alignment=0  # Left alignment
    )
    
    # Content for the PDF
    story = []
    
    # Title
    title = Paragraph("Data Ingestion and Processing Guide", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Introduction
    intro_title = Paragraph("Introduction", subtitle_style)
    story.append(intro_title)
    
    intro_text = Paragraph("""
    Data ingestion is a fundamental process in modern data analytics and machine learning workflows. 
    It involves collecting, importing, and processing data from various sources for immediate use or 
    storage in databases. This document provides an overview of key concepts, best practices, and 
    implementation strategies for effective data ingestion.
    """, body_style)
    story.append(intro_text)
    story.append(Spacer(1, 15))
    
    # Key Concepts
    concepts_title = Paragraph("Key Concepts", subtitle_style)
    story.append(concepts_title)
    
    concepts_text = Paragraph("""
    <b>1. Data Sources:</b> Data can originate from multiple sources including databases, APIs, 
    file systems, streaming platforms, and external services. Each source requires specific 
    handling methods and protocols.
    
    <b>2. Data Formats:</b> Common formats include JSON, CSV, XML, Parquet, and Avro. 
    Understanding format characteristics helps in choosing appropriate processing tools.
    
    <b>3. Data Quality:</b> Ensuring data accuracy, completeness, and consistency is crucial 
    for reliable analytics and decision-making processes.
    
    <b>4. Scalability:</b> Data ingestion systems must handle increasing data volumes while 
    maintaining performance and reliability.
    """, body_style)
    story.append(concepts_text)
    story.append(Spacer(1, 15))
    
    # Best Practices
    practices_title = Paragraph("Best Practices", subtitle_style)
    story.append(practices_title)
    
    practices_text = Paragraph("""
    • <b>Data Validation:</b> Implement comprehensive validation rules to ensure data quality
    • <b>Error Handling:</b> Design robust error handling mechanisms for failed ingestion attempts
    • <b>Monitoring:</b> Set up monitoring and alerting for ingestion pipelines
    • <b>Documentation:</b> Maintain clear documentation of data sources, schemas, and processes
    • <b>Security:</b> Implement appropriate security measures for sensitive data
    • <b>Backup Strategies:</b> Establish reliable backup and recovery procedures
    """, body_style)
    story.append(practices_text)
    story.append(Spacer(1, 15))
    
    # Implementation
    implementation_title = Paragraph("Implementation Strategies", subtitle_style)
    story.append(implementation_title)
    
    implementation_text = Paragraph("""
    <b>Batch Processing:</b> Suitable for large datasets that don't require real-time processing. 
    Examples include daily ETL jobs and bulk data imports.
    
    <b>Stream Processing:</b> Ideal for real-time data ingestion where low latency is critical. 
    Technologies like Apache Kafka and Apache Flink are commonly used.
    
    <b>Hybrid Approaches:</b> Combining batch and stream processing for optimal performance 
    and cost-effectiveness.
    """, body_style)
    story.append(implementation_text)
    story.append(Spacer(1, 15))
    
    # Conclusion
    conclusion_title = Paragraph("Conclusion", subtitle_style)
    story.append(conclusion_title)
    
    conclusion_text = Paragraph("""
    Effective data ingestion is the foundation of successful data-driven organizations. 
    By following best practices and choosing appropriate technologies, organizations can 
    build robust, scalable, and maintainable data ingestion pipelines that support 
    their analytical and operational needs.
    """, body_style)
    story.append(conclusion_text)
    
    # Build the PDF
    doc.build(story)
    print("PDF document 'sample_document.pdf' has been created successfully!")

if __name__ == "__main__":
    create_pdf() 