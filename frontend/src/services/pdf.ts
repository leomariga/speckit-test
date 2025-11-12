/**
 * PDF generation service using markdown-it and html2pdf.js
 */
import MarkdownIt from 'markdown-it';
import html2pdf from 'html2pdf.js';

interface ConversionOptions {
  filename?: string;
  margin?: number;
  format?: string;
}

class PdfService {
  private md: MarkdownIt;

  constructor() {
    this.md = new MarkdownIt({
      html: true,
      breaks: true,
      linkify: true,
    });
  }

  /**
   * Convert markdown text to HTML
   */
  markdownToHtml(markdown: string): string {
    return this.md.render(markdown);
  }

  /**
   * Convert markdown to PDF and download
   */
  async convertToPdf(
    markdown: string,
    options: ConversionOptions = {}
  ): Promise<{ success: boolean; pageCount: number; error?: string }> {
    try {
      // Convert markdown to HTML
      const htmlContent = this.markdownToHtml(markdown);

      // Create a container for the HTML content with print styles
      const container = document.createElement('div');
      container.className = 'pdf-content';
      container.innerHTML = htmlContent;
      document.body.appendChild(container);

      // PDF options
      const pdfOptions = {
        margin: options.margin || 10,
        filename: options.filename || 'markdown-export.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true },
        jsPDF: { unit: 'mm', format: options.format || 'a4', orientation: 'portrait' },
      };

      // Generate PDF
      const pdf = await html2pdf().set(pdfOptions).from(container).toPdf().get('pdf');
      
      // Get page count
      const pageCount = pdf.internal.getNumberOfPages();

      // Save PDF
      await html2pdf().set(pdfOptions).from(container).save();

      // Clean up
      document.body.removeChild(container);

      return { success: true, pageCount };
    } catch (error) {
      console.error('PDF conversion error:', error);
      return {
        success: false,
        pageCount: 0,
        error: error instanceof Error ? error.message : 'PDF conversion failed',
      };
    }
  }

  /**
   * Calculate page count from markdown (estimation)
   */
  estimatePageCount(markdown: string): number {
    // Rough estimation: ~50 lines per page
    const lines = markdown.split('\n').length;
    return Math.ceil(lines / 50);
  }

  /**
   * Validate markdown file
   */
  validateMarkdownFile(file: File): { valid: boolean; error?: string } {
    // Check file type
    const validExtensions = ['.md', '.markdown', '.txt'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!validExtensions.includes(fileExtension)) {
      return {
        valid: false,
        error: 'Invalid file type. Please upload a markdown file (.md, .markdown, or .txt)',
      };
    }

    // Check file size (max 5MB)
    const maxSize = 5 * 1024 * 1024; // 5MB
    if (file.size > maxSize) {
      return {
        valid: false,
        error: 'File too large. Maximum size is 5MB',
      };
    }

    return { valid: true };
  }

  /**
   * Read markdown file content
   */
  async readFileContent(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        const content = e.target?.result as string;
        resolve(content);
      };
      
      reader.onerror = () => {
        reject(new Error('Failed to read file'));
      };
      
      reader.readAsText(file);
    });
  }
}

export const pdfService = new PdfService();
export default pdfService;

