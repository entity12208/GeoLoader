#include <iostream>
#include <fstream>
#include <windows.h>
#include <direct.h>

void createDirectory(const std::string& path) {
    _mkdir(path.c_str());
}

void copyFile(const std::string& src, const std::string& dest) {
    std::ifstream srcFile(src, std::ios::binary);
    std::ofstream destFile(dest, std::ios::binary);
    destFile << srcFile.rdbuf();
}

void install() {
    std::string installPath = "C:\\Program Files\\GeoLoader";
    std::string binaryPath = "binaries\\geometry_dash.exe";

    createDirectory(installPath);
    copyFile(binaryPath, installPath + "\\geometry_dash.exe");

    std::cout << "Installation successful on Windows!" << std::endl;
}

int main() {
    install();
    return 0;
}
