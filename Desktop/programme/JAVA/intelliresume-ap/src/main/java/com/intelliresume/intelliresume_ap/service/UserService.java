package com.intelliresume.intelliresume_ap.service;

import com.intelliresume.intelliresume_ap.entity.User;
import com.intelliresume.intelliresume_ap.repository.UserRepository;
import com.intelliresume.intelliresume_ap.util.JwtUtil;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final AuthenticationManager authenticationManager;

    public UserService(UserRepository userRepository, PasswordEncoder passwordEncoder, JwtUtil jwtUtil, AuthenticationManager authenticationManager) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtUtil = jwtUtil;
        this.authenticationManager = authenticationManager;
    }

    public User registerUser(User user) {
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        return userRepository.save(user);
    }

    public String loginUser(String username, String password) {
        // 【核心战术变更！】我们命令“认证总管”去执行官方认证！
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(username, password)
        );

        // 如果上面没报错，说明认证成功！我们再去找用户、发Token。
        var user = userRepository.findByUsername(username);
        return jwtUtil.generateToken(user.getUsername());
    }
}