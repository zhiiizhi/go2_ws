cmake_minimum_required(VERSION 3.5)
project(teleop_twist_keyboard)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  ${PROJECT_NAME}/teleop_twist_keyboard
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
