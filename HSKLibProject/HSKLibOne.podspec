
Pod::Spec.new do |s|

  s.name         = "HSKLibOne"
  s.version      = "0.0.1"
  s.summary      = "A short description of HSKLibOne."


  s.author       = { "leigaopan" => "leigaopan@youyuwo.com" }
  s.platform     = :ios, "8.0"
  s.source       = { :git => "http://EXAMPLE/HSKLibOne.git", :tag => "#{s.version}" }

  s.source_files = "HSKLibProject/HSKLibOne", "HSKLibProject/HSKLibOne/**/*.{h,m}"
  s.public_header_files = "HSKLibProject/HSKLibOne/HSKLibOne.h", "HSKLibProject/HSKLibOne/HSKFirstLib.h"
end
