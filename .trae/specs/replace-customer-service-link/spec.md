# 获客链接替换 - 产品需求文档

## Overview
- **Summary**: 替换小程序中的客服联系方式为新的获客链接 `https://work.weixin.qq.com/ca/cawcde4716ce3659af`，并在我的页面添加联系客服按钮。
- **Purpose**: 统一客服联系方式，通过获客链接引导用户添加企业微信，提高客服转化率。
- **Target Users**: 使用AI自动账小程序的用户。

## Goals
- 替换小程序中所有客服联系方式为新的获客链接
- 在我的页面添加联系客服按钮，引导用户添加企业微信
- 确保所有客服联系方式保持一致

## Non-Goals (Out of Scope)
- 修改客服的实际联系方式（仅修改链接和显示文本）
- 更改其他功能模块的内容
- 优化获客链接本身的设计

## Background & Context
- 已创建新的获客链接：`https://work.weixin.qq.com/ca/cawcde4716ce3659af`
- 该链接用于引导用户添加企业微信客服
- 需要在小程序中统一使用该链接，确保用户体验一致

## Functional Requirements
- **FR-1**: 替换产品页面中的客服联系方式为新的获客链接
- **FR-2**: 替换指南页面中的客服联系方式为新的获客链接
- **FR-3**: 在我的页面添加联系客服按钮，链接到新的获客链接
- **FR-4**: 确保所有客服联系方式的显示文本保持一致

## Non-Functional Requirements
- **NFR-1**: 链接替换后应保持页面布局美观
- **NFR-2**: 联系客服按钮应易于识别和点击
- **NFR-3**: 链接跳转应流畅，无卡顿

## Constraints
- **Technical**: 小程序平台限制，需要使用 `wx.navigateTo` 或 `wx.navigateToMiniProgram` 等API跳转
- **Business**: 获客链接为固定地址，不可修改

## Assumptions
- 获客链接 `https://work.weixin.qq.com/ca/cawcde4716ce3659af` 可以正常访问
- 该链接可以正确引导用户添加企业微信

## Acceptance Criteria

### AC-1: 产品页面客服联系方式替换
- **Given**: 用户打开产品页面
- **When**: 用户点击客服联系方式或复制客服名称
- **Then**: 显示的客服名称应为"AI自动账客服"，复制的内容应为"AI自动账客服"
- **Verification**: `human-judgment`

### AC-2: 指南页面客服联系方式替换
- **Given**: 用户打开指南页面
- **When**: 用户点击客服联系方式或复制客服名称
- **Then**: 显示的客服名称应为"AI自动账客服"，复制的内容应为"AI自动账客服"
- **Verification**: `human-judgment`

### AC-3: 我的页面添加联系客服按钮
- **Given**: 用户打开我的页面
- **When**: 用户点击联系客服按钮
- **Then**: 应跳转到获客链接 `https://work.weixin.qq.com/ca/cawcde4716ce3659af`
- **Verification**: `programmatic`

### AC-4: 所有页面客服联系方式一致
- **Given**: 用户浏览不同页面
- **When**: 用户查看客服联系方式
- **Then**: 所有页面显示的客服名称和链接应保持一致
- **Verification**: `human-judgment`

## Open Questions
- [ ] 获客链接是否需要在小程序内打开，还是跳转到外部浏览器？
- [ ] 联系客服按钮的具体位置和样式如何设计？