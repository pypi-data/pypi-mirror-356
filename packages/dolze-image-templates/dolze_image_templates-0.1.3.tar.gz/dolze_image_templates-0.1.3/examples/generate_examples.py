"""
Example script demonstrating how to use the Dolze Templates library.

This script shows how to:
1. Load templates from JSON files
2. Render templates with different data
3. Save the generated images
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import the package
import sys

sys.path.append(str(Path(__file__).parent.parent))

from dolze_image_templates import TemplateRegistry, get_template_registry, configure

# Configure the library
configure(
    templates_dir=os.path.join(
        os.path.dirname(__file__), "..", "dolze_image_templates", "templates"
    ),
    output_dir=os.path.join(os.path.dirname(__file__), "output"),
)


def generate_business_template(templateName: str):
    """Generate a business template post."""
    # Get the template registry
    registry = get_template_registry()
    template_data = {
        "cta_text": "LEARN MORE",
        "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
        "image_url": "https://www.calendar.com/wp-content/uploads/2019/09/CalendarAndroidApp.png.webp",
        "cta_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
        "heading": "plan your day in a snap",
        "subheading": "Driving success",
        "contact_email": "contact@business.com",
        "contact_phone": "+1-800-555-1234",
        "website_url": "dolze.ai /download",
        "quote": "The only way to do great work is to love what you do.",
        "theme_color": "#44EC9D",
        "user_avatar": "https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
        "user_name": "Alex Johnson",
        "user_title": "Marketing Director, TechCorp",
        "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
    }
    # Template data mapping
    if templateName == "calendar_app_promo":
        template_data = {
            "cta_text": "LEARN MORE",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "image_url": "https://www.calendar.com/wp-content/uploads/2019/09/CalendarAndroidApp.png.webp",
            "cta_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
            "heading": "plan your day in a snap",
            "subheading": "Driving your success forward",
            "contact_email": "contact@business.com",
            "contact_phone": "+1-800-555-1234",
            "website_url": "dolze.ai /download",
            "quote": "The only way to do great work is to love what you do.",
            "theme_color": "#44EC9D",
            "user_avatar": "https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "user_name": "Alex Johnson",
            "user_title": "Marketing Director, TechCorp",
            "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
        }
    elif templateName == "testimonials_template":
        template_data = {
            # Common fields
            "theme_color": "#44EC9D",
            "website_url": "dolze.ai/download",
            # Testimonials specific
            "user_avatar": "https://img.freepik.com/free-vector/isolated-young-handsome-man-different-poses-white-background-illustration_632498-859.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "user_name": "Sarah Johnson",
            "user_title": "Verified Buyer",
            "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
        }
    elif templateName == "blog_post" or templateName == "blog_post_2":
        template_data = {
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
            "title": "How to be environment conscious without being weird",
            "author": "@username",  # to be inserted by db
            "read_time": "4",
            "image_url": "https://img.freepik.com/free-vector/underwater-ocean-reef-coral-background_107791-1853.jpg",
            "logo_url": "https://img.freepik.com/free-vector/gradient-s-letter-logo_343694-1365.jpg",
        }
    elif (
        templateName == "qa_template"
        or templateName == "qa_template_2"
        or templateName == "qa_template_3"
    ):
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "question": "What is Title?",
            "answer": "One wind turbine can produce enough electricity to power around 1,500 homes annually!",
            "username": "@username",
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
        }
    elif templateName == "quote_template" or templateName == "quote_template_2":
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "quote1": "The only way to do",
            "quote2": "great work is to love what you do",
            "username": "@stevejobs",
            "website_url": "www.example.com",
            "theme_color": "#44EC9D",
        }
    elif templateName == "education_info" or templateName == "education_info_2":
        template_data = {
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
            "testimonial_text": "One wind turbine can produce enough electricity to power around 1,500 homes annually!",
            "author": "@username",  # to be inserted by db
            "read_time": "4",
            "image_url": "https://img.freepik.com/free-photo/portrait-young-businesswoman-holding-eyeglasses-hand-against-gray-backdrop_23-2148029483.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "logo_url": "https://img.freepik.com/free-vector/gradient-s-letter-logo_343694-1365.jpg",
        }
    elif templateName == "product_promotion_2":
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?w=200&h=200&white=true",
            "image_url": "https://media.licdn.com/dms/image/v2/D4D12AQGnbgq78a4LMg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1677634984855?e=1755734400&v=beta&t=PS0JBTOx91C-z1Tb4Ky4NOnQeRosuW-7i1GIDUj088o",
            "quote1": "the kanban board",
            "quote2": "you'll absolutely love",
        }
    elif (
        templateName == "product_showcase"
        or templateName == "product_showcase_2"
        or templateName == "product_showcase_3"
    ):
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?w=200&h=200&white=true",
            "product_image": "https://media.istockphoto.com/id/171384959/photo/executive-office-chair.jpg?s=612x612&w=0&k=20&c=5vRz91x_JdXHGrzWoDxtj7xEYvI35ls3pDfysHgd57M=",
            "product_name": "Strong chair",
            "product_price": "$52",
            "product_description": "made with highly refined wood",
            "theme_color": "#44EC9D",
            "badge_text": "Bestseller",
        }

    # Render the template with the data
    output_path = os.path.join("output", f"{templateName}.png")
    rendered_image = registry.render_template(
        templateName,
        template_data,
        output_path=output_path,
    )

    print(f"Template saved to {os.path.abspath(output_path)}")
    return rendered_image


def main():
    """Generate all example templates."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Generate all templates
        templates = [
            "calendar_app_promo",
            "testimonials_template",
            "blog_post",
            "blog_post_2",
            "education_info",
            "product_promotion_2",
            "promotional_banner",
            "product_promotion",
            "qa_template",
            "quote_template",
            "quote_template_2",
            "product_showcase",
            "testimonials_template_2",
            "product_showcase_2",
            "product_showcase_3",
            "qa_template_2",
            "qa_template",
            "qa_template_3",
            "education_info",
            "education_info_2",
        ]
        for template in templates:
            generate_business_template(template)

        print("\nAll examples generated successfully!")
    except Exception as e:
        print(f"\nError generating examples: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
