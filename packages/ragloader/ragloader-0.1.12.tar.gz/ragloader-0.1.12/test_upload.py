from ragloader.orchestrator import UploadOrchestrator

def main():
    data_dir = "book_data"

    orchestrator = UploadOrchestrator(
        data_directory=data_dir,
        config='config_pdf_semantic.toml',
        initialize_collections=True
    )
    orchestrator.upload()

if __name__ == "__main__":
    main()