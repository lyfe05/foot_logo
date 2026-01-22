import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import time

def fetch_football_logos():
    base_url = "https://football-logos.cc/all/"
    total_logos = 0
    
    try:
        # Open the output file once
        with open('logos.txt', 'w', encoding='utf-8') as txt_file:
            # Write header
            txt_file.write("Football Logos Collection\n")
            txt_file.write("=" * 60 + "\n\n")
            
            # Fetch pages from 0 to 45
            for page_num in range(0, 46):  # 0 to 45 inclusive
                if page_num == 0:
                    url = f"{base_url}"
                else:
                    url = f"{base_url}{page_num}/"
                
                print(f"Fetching page {page_num}...")
                
                try:
                    # Fetch the webpage
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    # Parse HTML content
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find all image tags
                    images = soup.find_all('img')
                    
                    page_logos = 0
                    for img in images:
                        src = img.get('src')
                        alt = img.get('alt', 'No description')
                        
                        if src:
                            # Convert relative URLs to absolute URLs
                            full_url = urljoin(url, src)
                            total_logos += 1
                            page_logos += 1
                            
                            # Write to file
                            txt_file.write(f"Logo {total_logos}:\n")
                            txt_file.write(f"  Page: {page_num}\n")
                            txt_file.write(f"  Description: {alt}\n")
                            txt_file.write(f"  URL: {full_url}\n")
                            txt_file.write(f"  Filename: {os.path.basename(full_url)}\n")
                            txt_file.write("-" * 30 + "\n")
                    
                    print(f"  Found {page_logos} images on page {page_num}")
                    
                    # Small delay to be respectful to the server
                    time.sleep(0.5)
                    
                except requests.RequestException as e:
                    print(f"  Error fetching page {page_num}: {e}")
                    continue  # Continue with next page even if one fails
            
            # Write summary
            txt_file.write("\n" + "=" * 60 + "\n")
            txt_file.write(f"Total logos found across all pages: {total_logos}\n")
        
        print(f"\n{'='*60}")
        print(f"Total logos found: {total_logos}")
        print(f"All logos saved to logos.txt")
        
        return total_logos
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def download_logos():
    """Download logos from all pages"""
    base_url = "https://football-logos.cc/all/"
    downloaded_count = 0
    
    try:
        # Create directory for logos
        os.makedirs('football_logos', exist_ok=True)
        
        # Fetch pages from 0 to 45
        for page_num in range(0, 46):  # 0 to 45 inclusive
            if page_num == 0:
                url = f"{base_url}"
            else:
                url = f"{base_url}{page_num}/"
            
            print(f"\nProcessing page {page_num}...")
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                images = soup.find_all('img')
                
                for i, img in enumerate(images):
                    src = img.get('src')
                    if src:
                        full_url = urljoin(url, src)
                        
                        try:
                            img_response = requests.get(full_url)
                            img_response.raise_for_status()
                            
                            # Get file extension and create filename
                            filename = f"football_logos/logo_{downloaded_count + 1}_{os.path.basename(full_url)}"
                            
                            # Save the image
                            with open(filename, 'wb') as f:
                                f.write(img_response.content)
                            
                            downloaded_count += 1
                            print(f"  Downloaded: {filename}")
                            
                        except Exception as e:
                            print(f"  Error downloading {full_url}: {e}")
                
                # Small delay to be respectful to the server
                time.sleep(0.5)
                
            except Exception as e:
                print(f"  Error processing page {page_num}: {e}")
                continue  # Continue with next page even if one fails
        
        print(f"\nTotal logos downloaded: {downloaded_count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Fetching football logos from all pages (0 to 45)")
    print("=" * 60)
    
    # Display logo information from all pages (saved to logos.txt)
    total_logos = fetch_football_logos()
    
    if total_logos > 0:
        # Ask if user wants to download
        choice = input("\nDo you want to download all logos? (y/n): ")
        if choice.lower() == 'y':
            print("\nDownloading logos from all pages...")
            download_logos()
    else:
        print("\nNo logos found to download.")
