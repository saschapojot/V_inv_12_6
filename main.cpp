#include "./mc_subroutine/mc_read_load_compute.hpp"


///
/// @param left
/// @param right
/// @return random number ~ U(left, right)
double gen_uni_open(const double &left, const double &right){
    std::random_device rd;
    std::ranlux24_base e2(rd());
    double unif_left_end_double_on_the_right=std::nextafter(left, std::numeric_limits<double>::infinity());
    std::uniform_real_distribution<> distUnif(unif_left_end_double_on_the_right,right); //[unif_left_end_double_on_the_right, unif_right_end)
    double xNext=distUnif(e2);
    return xNext;
}


void saveArrayToCSV(const std::shared_ptr<double[]>& array, const  size_t& arraySize, const std::string& filename){

    std::ofstream outFile(filename);

    if (!outFile.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }
    outFile << std::setprecision(std::numeric_limits<double>::digits10 + 1) << std::fixed;
    outFile<<"rand_data"<<"\n";

    for(size_t i=0;i<arraySize;i++){
        outFile<<array[i]<<"\n";

    }
    outFile.close();




}
//This file tests if the random numbers are on open interval
int main(int argc, char *argv[]) {
    size_t loopToWrite = 1000000;

    std::shared_ptr<double[]> x_ptr = std::shared_ptr<double[]>(new double[loopToWrite],
                                                                std::default_delete<double[]>());

    const auto tGenStart{std::chrono::steady_clock::now()};

    double left=0;
    double right=1;
    for (size_t i=0;i<loopToWrite;i++){
        x_ptr[i]=gen_uni_open(left,right);
    }

    std::string fileName="rand.csv";

    saveArrayToCSV(x_ptr,loopToWrite,fileName);
    const auto tGenEnd{std::chrono::steady_clock::now()};
    const std::chrono::duration<double> elapsed_secondsAll{tGenEnd - tGenStart};
    std::cout<<"time: "<<elapsed_secondsAll.count()<<" s"<<std::endl;

}