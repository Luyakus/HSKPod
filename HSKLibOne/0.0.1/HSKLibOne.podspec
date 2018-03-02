
Pod::Spec.new do |s|

  s.name         = "HSKLibOne"
  s.version      = "0.0.1"
  s.summary      = "HSKLibOne is a test private pod"
  s.license      = "MIT"
  s.homepage     = "https://luyakus.github.io/"
  s.author       = { "leigaopan" => "leigaopan@youyuwo.com" }
  s.platform     = :ios, "8.0"
  s.source       = { :git => "https://github.com/Luyakus/HSKPod.git" }

  s.source_files = "HSKLibProject/HSKLibOne/**/*.{h,m}"
  s.public_header_files = "HSKLibPorject/HSKLibOne/HSKLibOne.h"
end
