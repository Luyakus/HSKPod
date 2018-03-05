//
//  ViewController.m
//  HSKShellProject
//
//  Created by Sam on 02/03/2018.
//  Copyright © 2018 Sam. All rights reserved.
//

#import "ViewController.h"
#import "HSKLibOne.h"
@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    [HSKFirstLib doSomething];
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}


@end
