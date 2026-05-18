"""
Modulo per la generazione di report
Supporta output in JSON, TXT e PDF
"""

import json
import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, 
    TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class ReportGenerator:
    """
    Classe per generare report professionali delle ricerche OSINT
    """
    
    def __init__(self, data, target):
        self.data = data
        self.target = target
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.reports_dir = "reports"
        
        # Crea la cartella reports se non esiste
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def to_json(self, filename=None):
        """
        Genera un report in formato JSON
        """
        if not filename:
            filename = f"osint_report_{self.target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.reports_dir, f"{filename}.json")
        
        report_data = {
            'report_metadata': {
                'target': self.target,
                'generated_at': self.timestamp,
                'tool': 'OSINT CLI Framework v1.0',
                'author': 'Generated automatically'
            },
            'results': self.data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def to_txt(self, filename=None):
        """
        Genera un report in formato TXT (testo leggibile)
        """
        if not filename:
            filename = f"osint_report_{self.target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.reports_dir, f"{filename}.txt")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 80 + "\n")
            f.write(" " * 25 + "OSINT REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Target: {self.target}\n")
            f.write(f"Generated: {self.timestamp}\n")
            f.write(f"Tool: OSINT CLI Framework v1.0\n")
            f.write("-" * 80 + "\n\n")
            
            # Risultati per modulo
            for module_name, module_data in self.data.items():
                f.write(f"\n{'=' * 80}\n")
                f.write(f"MODULO: {module_name.upper()}\n")
                f.write(f"{'=' * 80}\n\n")
                
                if isinstance(module_data, dict):
                    for key, value in module_data.items():
                        f.write(f"{key.upper()}:\n")
                        if isinstance(value, list):
                            for item in value:
                                f.write(f"  - {item}\n")
                        elif isinstance(value, dict):
                            for k, v in value.items():
                                f.write(f"  {k}: {v}\n")
                        else:
                            f.write(f"  {value}\n")
                        f.write("\n")
                else:
                    f.write(f"{str(module_data)}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")
        
        return filepath
    
    def to_pdf(self, filename=None):
        """
        Genera un report professionale in formato PDF
        """
        if not filename:
            filename = f"osint_report_{self.target}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = os.path.join(self.reports_dir, f"{filename}.pdf")
        
        # Crea il documento PDF
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Stili
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#16213e'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        normal_style = styles["Normal"]
        normal_style.fontSize = 10
        
        # Contenuto
        story = []
        
        # Titolo
        story.append(Paragraph("OSINT REPORT", title_style))
        story.append(Spacer(1, 20))
        
        # Info generali
        info_data = [
            ['Target:', self.target],
            ['Generated:', self.timestamp],
            ['Tool:', 'OSINT CLI Framework v1.0'],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8e8e8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Risultati per modulo
        for module_name, module_data in self.data.items():
            story.append(PageBreak())
            story.append(Paragraph(f"MODULO: {module_name.upper()}", heading_style))
            story.append(Spacer(1, 12))
            
            if isinstance(module_data, dict):
                for key, value in module_data.items():
                    story.append(Paragraph(f"<b>{key.upper()}</b>", styles['Heading3']))
                    
                    if isinstance(value, list):
                        if value:
                            list_data = [[str(item)] for item in value]
                            list_table = Table(list_data, colWidths=[6*inch])
                            list_table.setStyle(TableStyle([
                                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
                                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                ('FONTSIZE', (0, 0), (-1, -1), 9),
                                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                                ('TOPPADDING', (0, 0), (-1, -1), 6),
                                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                            ]))
                            story.append(list_table)
                        else:
                            story.append(Paragraph("<i>Nessun dato disponibile</i>", normal_style))
                    
                    elif isinstance(value, dict):
                        dict_data = [[str(k), str(v)] for k, v in value.items()]
                        dict_table = Table(dict_data, colWidths=[2*inch, 4*inch])
                        dict_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 0), (-1, -1), 9),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                            ('LEFTPADDING', (0, 0), (-1, -1), 8),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                            ('TOPPADDING', (0, 0), (-1, -1), 5),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                        ]))
                        story.append(dict_table)
                    
                    else:
                        story.append(Paragraph(str(value), normal_style))
                    
                    story.append(Spacer(1, 8))
            else:
                story.append(Paragraph(str(module_data), normal_style))
        
        # Footer
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "<i>Report generated by OSINT CLI Framework - For educational purposes only</i>",
            ParagraphStyle('Footer', parent=normal_style, alignment=TA_CENTER, textColor=colors.grey)
        ))
        
        # Genera PDF
        doc.build(story)
        
        return filepath