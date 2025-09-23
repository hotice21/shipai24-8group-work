package com.intelliresume.intelliresume_ap.entity;

import jakarta.persistence.*; // 这是JPA的核心武器库！
import lombok.Data; // 我们的“言灵法师”Lombok！

@Entity // 咒语1：盖章！声明“我是一个实体类，对应数据库里的一张表”
@Table(name = "users") // 咒语2：指定这张表在数据库里的名字叫“users”(推荐用复数)
@Data // 咒语3：Lombok大神！请自动帮我生成所有啰嗦的get/set等方法！
public class User {

    @Id // 咒语4：标记！下面的这个字段是“主键”，是每个用户的唯一身份证号！
    @GeneratedValue(strategy = GenerationType.IDENTITY) // 咒语5：自增！这个ID不需要我们操心，数据库会自动帮我们一个一个往上加 (1, 2, 3...)
    private Long id;

    @Column(nullable = false, unique = true) // 咒语6：约束！这个字段不能为空，并且必须是唯一的，不能有两个人用同一个用户名
    private String username;

    @Column(nullable = false) // 咒语7：约束！密码不能为空
    private String password;

    @Column(unique = true) // 咒语8：约束！邮箱可以是空的，但如果要填，就必须是唯一的
    private String email;

}