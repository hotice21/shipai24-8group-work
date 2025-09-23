package com.intelliresume.intelliresume_ap.filter;

import com.intelliresume.intelliresume_ap.util.JwtUtil;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.lang.NonNull;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component // 咒语1：报告SpringBoot！我是一个重要的“安保组件”，请管理我！
public class JwtRequestFilter extends OncePerRequestFilter {

    private final JwtUtil jwtUtil;
    private final UserDetailsService userDetailsService; // 咒语2：神盾局的“户籍管理员”

    // 使用“构造函数注入”，把需要的工具都拿过来！
    public JwtRequestFilter(JwtUtil jwtUtil, UserDetailsService userDetailsService) {
        this.jwtUtil = jwtUtil;
        this.userDetailsService = userDetailsService;
    }

    @Override
    protected void doFilterInternal(
            @NonNull HttpServletRequest request,
            @NonNull HttpServletResponse response,
            @NonNull FilterChain filterChain) throws ServletException, IOException {

        final String authHeader = request.getHeader("Authorization"); // 从请求头里，把“Authorization”字段拿出来
        final String jwt;
        final String username;

        // 步骤1：检查请求头，如果里面没有Authorization，或者不以"Bearer "开头，直接放行！
        // (为什么放行？因为后面的安保流程还会再检查一次，确保这条路是公共路径还是戒严区)
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        // 步骤2：如果请求头格式正确，就把真正的JWT通行证“抠”出来
        jwt = authHeader.substring(7); // "Bearer "后面就是JWT，所以从第7个字符开始截取

        // 步骤3：用我们的JWT工具箱，从通行证里解析出“用户名”
        username = jwtUtil.extractUsername(jwt);

        // 步骤4：核心验证！
        // username不为空 -> 确保我们成功解析出了用户名
        // SecurityContextHolder.getContext().getAuthentication() == null -> 确保这个用户“尚未登录”
        // (这是为了防止重复验证)
        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {

            // 步骤4A：让“户籍管理员”根据用户名，去数据库里查出这位用户的详细档案
            var userDetails = this.userDetailsService.loadUserByUsername(username);

            // 步骤4B：用JWT工具箱，验证“通行证”是否有效（签名对不对？有没有过期？用户名匹不匹配？）
            if (jwtUtil.isTokenValid(jwt, userDetails.getUsername())) {
                // 步骤4C：如果通行证有效，就创建一个“认证凭证”
                UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                );
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));

                // 步骤4D：【最关键的一步！】把这个“认证凭证”，正式地存入“神盾局的安保上下文”里！
                // 这一步，就相当于哨兵在系统里，为这位通过验证的用户，正式地盖了一个“已认证”的章！
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        // 步骤5：不管前面发生了什么，最后都要放行，让请求继续走下去。
        // (如果上面盖章成功了，那它就能进入戒严区；如果没成功，那它依然会被神盾局的最终防线拦住)
        filterChain.doFilter(request, response);
    }
}
