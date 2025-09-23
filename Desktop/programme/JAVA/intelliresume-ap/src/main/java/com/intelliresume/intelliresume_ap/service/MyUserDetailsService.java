package com.intelliresume.intelliresume_ap.service;

import com.intelliresume.intelliresume_ap.repository.UserRepository;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Collections;

@Service
public class MyUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    public MyUserDetailsService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // 这就是具体的工作逻辑：
        // 根据用户名，命令“数据管家”去数据库里查
        com.intelliresume.intelliresume_ap.entity.User user = userRepository.findByUsername(username);

        if (user == null) {
            // 如果查不到，就必须抛出这个特定的异常，神盾局会捕获并处理它
            throw new UsernameNotFoundException("User not found with username: " + username);
        }

        // 如果查到了，就把它转换成Spring Security能看懂的UserDetails对象
        // 第一个参数：用户名
        // 第二个参数：加密后的密码 (非常重要！神盾局内部需要用它来做一些比对)
        // 第三个参数：权限列表 (我们暂时给个空的)
        return new User(user.getUsername(), user.getPassword(), Collections.emptyList());
    }
}