package com.intelliresume.intelliresume_ap.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable; // 导入新武器！
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    // 注意看！URL变了，后面多了个“花括号”
    @GetMapping("/hello/{name}")
    public String sayHelloToSomeone(@PathVariable String name) { // 方法参数也变了！
        return "Hello, " + name + "! Welcome to the IntelliResume world!";
    }
    @GetMapping("/goodbye/{name}")
    public String sayGoodbyeToSomeone(@PathVariable String name){
        return "Goodbye,"+ name +"! My friend! See you next time!";
    }
}