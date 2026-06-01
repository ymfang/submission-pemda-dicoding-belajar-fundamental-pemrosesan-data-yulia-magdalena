from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv


def run_etl():
    raw_data = scrape_main()

    print(f"Total raw data: {len(raw_data)}")

    clean_data = transform_data(raw_data)

    print(f"Total clean data: {len(clean_data)}")

    if clean_data.empty:
        print("No clean data to save")
        return

    is_saved = save_to_csv(clean_data, "products.csv")

    if is_saved:
        print("Data berhasil disimpan ke products.csv")
    else:
        print("Gagal menyimpan data ke CSV")


if __name__ == "__main__":
    run_etl()