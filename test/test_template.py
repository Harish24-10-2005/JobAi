"""
Test the resume template integration
"""
import asyncio
from src.services.resume_service import resume_service


async def test_templates():
    print("=" * 50)
    print("Testing Resume Template Integration")
    print("=" * 50)
    
    # Test getting all templates
    print("\n1. Fetching all templates from Supabase...")
    templates = await resume_service.get_templates()
    if templates:
        print(f"   Found {len(templates)} templates:")
        for t in templates:
            desc = t.get("description", "No description")[:50]
            print(f"   - {t['name']}: {desc}...")
    else:
        print("   No templates found (check Supabase connection)")
    
    # Test getting Harish Pro template
    print("\n2. Testing template lookup...")
    template = None
    for t_type in ['harish', 'pro', 'ats']:
        t = await resume_service.get_template_by_type(t_type)
        if t:
            print(f"   ✅ Found '{t_type}': {t['name']}")
            template = t
            break
        else:
            print(f"   ❌ '{t_type}' not found")
    
    # Get default if none found
    if not template:
        print("\n   Trying default template...")
        template = await resume_service.get_default_template()
        if template:
            print(f"   ✅ Found default: {template['name']}")
    
    # Test fill_template
    print("\n3. Testing template filling...")
    if template:
        test_profile = {
            "personal_information": {
                "full_name": "Harish R",
                "email": "harish@example.com",
                "phone": "+91 88076 39930",
                "linkedin": "https://linkedin.com/in/harish",
                "github": "https://github.com/Harish24-10-2005",
                "portfolio": "https://harishravikumar.netlify.app/"
            },
            "skills": {
                "primary": ["Python", "C++", "LangChain"],
                "secondary": ["Docker", "FastAPI"],
                "tools": ["Git", "MongoDB"]
            },
            "experience": [
                {
                    "company": "INEUDATA",
                    "title": "Data Engineering Intern",
                    "dates": "2025",
                    "location": "",
                    "highlights": [
                        "Designed scalable ETL pipelines with Apache Kafka and PySpark",
                        "Automated 40% of manual workflows"
                    ]
                }
            ],
            "education": [
                {
                    "institution": "Sri Eshwar College of Engineering",
                    "degree": "B.Tech",
                    "field_of_study": "AI and Data Science",
                    "dates": "2023-2027",
                    "gpa": "8.34"
                }
            ],
            "projects": [
                {
                    "name": "Sketch Mentor",
                    "technologies": ["Python", "QLoRA"],
                    "url": "https://github.com/example",
                    "description": ["Fine-tuned Qwen2.5 model to 95% accuracy"]
                }
            ],
            "summary": "AI/ML Engineer with expertise in LangChain, deep learning, and distributed systems."
        }
        
        # No tailored content, use profile directly
        filled = resume_service.fill_template(
            template.get("latex_content", ""),
            test_profile,
            test_profile  # Same as profile
        )
        
        # Check placeholders
        latex = template.get("latex_content", "")
        print(f"\n   Template uses placeholders:")
        print(f"   - <<NAME>>: {'<<NAME>>' in latex}")
        print(f"   - {{{{FULL_NAME}}}}: {'{{FULL_NAME}}' in latex}")
        
        # Check what was replaced
        print(f"\n   After filling:")
        print(f"   - Name present: {'Harish R' in filled}")
        print(f"   - Email present: {'harish@example.com' in filled}")
        print(f"   - Skills present: {'Python' in filled}")
        
        # Show first part of filled template
        doc_start = filled.find("\\begin{document}")
        if doc_start > 0:
            print("\n4. Sample of filled content:")
            print("-" * 40)
            sample = filled[doc_start:doc_start+600]
            print(sample)
            print("...")
    else:
        print("   ⚠️ No template available to test")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_templates())
