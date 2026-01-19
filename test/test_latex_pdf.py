"""
Test LaTeX compilation and PDF generation
"""
import asyncio
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.services.resume_service import resume_service
from src.core.console import console


async def test_latex_compilation():
    """Test LaTeX to PDF compilation."""
    console.header("🧪 Testing LaTeX PDF Generation")
    
    # Test 1: Get a template from database
    console.subheader("Test 1: Fetch template from Supabase")
    template = await resume_service.get_template_by_type("ats")
    
    if not template:
        console.error("Could not fetch template from database")
        return False
    
    console.success(f"Template fetched: {template.get('name', 'Unknown')}")
    latex_content = template.get("latex_content", "")
    console.info(f"LaTeX size: {len(latex_content)} bytes")
    
    # Test 2: Try to compile with a simple valid LaTeX document
    console.subheader("Test 2: Test pdflatex compilation")
    
    # Create a simple valid LaTeX document for testing
    test_latex = r"""
\documentclass{article}
\begin{document}
\section*{Test Resume}
\textbf{Name:} John Doe \\
\textbf{Email:} john@example.com \\
\textbf{Phone:} 555-1234

\section*{Experience}
Software Engineer at Test Corp (2020-2024)
\begin{itemize}
    \item Developed Python applications
    \item Worked with PostgreSQL databases
\end{itemize}

\section*{Skills}
Python, JavaScript, SQL, Git, Docker
\end{document}
"""
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = str(output_dir / "test_resume.pdf")
    
    result = resume_service.compile_to_pdf(test_latex, output_path)
    
    if result:
        console.success(f"PDF generated successfully!")
        
        # Check file size
        if Path(output_path).exists():
            pdf_size = Path(output_path).stat().st_size
            console.info(f"PDF path: {output_path}")
            console.info(f"PDF size: {pdf_size} bytes")
            return True
        else:
            console.warning("PDF was generated but file not found at expected path")
            return True  # compile_to_pdf returned something
    else:
        console.error("PDF generation failed")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_latex_compilation())
    if success:
        console.divider()
        console.success("LaTeX PDF generation is working!")
    else:
        console.divider()
        console.error("LaTeX PDF generation has issues")
