from summarizer.fetcher import fetch_web_content, format_links
from summarizer.summarizer import get_relevant_links
from summarizer.brochure import generate_brochure
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

logger = logging.getLogger(__name__)

def save_brochure_as_pdf(brochure_text, filename="brochure.pdf"):
    """Converts the brochure text to a PDF and saves it locally."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40  # Start position from the top

    for line in brochure_text.split("\n"):
        c.drawString(40, y_position, line)  # Draw text line by line
        y_position -= 20  # Move down for next line
        if y_position < 40:  # Prevent writing beyond the page
            c.showPage()
            y_position = height - 40

    c.save()
    logger.info(f"Brochure saved as {filename}")


def main():
    company_name = input("Enter company name: ") or "Aucleus"
    url = input("Enter company website: ") or "https://aucleus.com/"
    
    model_choice = input("Enter LLM model (default:gpt-4, deepseek-r1:1.5B): ") or "gpt-4"
    provider_choice = input("Enter provider (openai/ollama(ollama_lib/ollama_api), default: openai): ") or "openai"

    logger.info(f"Fetching links from {url}...")
    links = fetch_web_content(url)

    if not links:
        logger.error("No links found. Exiting...")
        return

    formatted_links = format_links(url, links)
    logger.info(f"Extracted and formatted {len(formatted_links)} links.")

    relevant_links = get_relevant_links(company_name, formatted_links, model=model_choice, provider=provider_choice)
    logger.info("Filtered relevant links.")

    brochure = generate_brochure(company_name, relevant_links, model=model_choice, provider=provider_choice)
    print("\nGenerated Brochure:\n")
    print(brochure)
    
    # Save brochure as PDF
    save_brochure_as_pdf(brochure, filename=f"{company_name}_brochure.pdf")

if __name__ == "__main__":
    main()