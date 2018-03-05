//
//  ViewController.m
//  HSKShellProject
//
//  Created by Sam on 28/02/2018.
//  Copyright © 2018 Sam. All rights reserved.
//

#import "ViewController.h"
#import "HSKLibProject.h"
@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    [HSKLibProject doSomething];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
