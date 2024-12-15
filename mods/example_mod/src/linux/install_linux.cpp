#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include <unistd.h>

void createDirectory(const std::string& path) {
    mkdir(path.c_str(), 0755);
}

void copyFile(const std::string& src, const std::string& dest) {
    std::ifstream srcFile(src, std::ios::binary);
    std::ofstream destFile(dest, std::ios::binary);
    destFile << srcFile.rdbuf();
}

void install() {
    std::string installPath = "/usr/local/geoloader";
    std::string binaryPath = "binaries/geometry_dash_linux";

    createDirectory(installPath);
    copyFile(binaryPath, installPath + "/geometry_dash");
    chmod((installPath + "/geometry_dash").c_str(), 0755);

    std::cout << "Installation successful on Linux!" << std::endl;
}

int main() {
    install();
    return 0;
}
