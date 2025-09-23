package com.intelliresume.intelliresume_ap.repository;

import com.intelliresume.intelliresume_ap.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, Long> {

    // 里面是空的！一个方法都不用写！
    User findByUsername(String username);

}