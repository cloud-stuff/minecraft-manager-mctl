class BaseInstaller:
    name: str

    def get_download_url(self, version: str) -> str:
        """
        Return the URL to download the server jar for the given version.
        :param version:
        :return:
        """
        raise NotImplementedError

    def get_file_name(self, version: str) -> str:
        """
        Returns file name for caching.
        :param version:
        :return:
        """
        return f"{self.name}-{version}.jar"
