---
paths:
  - "**/*.cs"
---

<!-- Generated from harness/github-copilot/instructions/csharp-ja.instructions.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

> **Scope.** Enforces Japanese C# and ASP.NET Core application conventions for modern C# 14, formatting, nullable references, EF Core, authentication, validation, OpenAPI, logging, testing, performance, and deployment.

# C# アプリケーション規約 — ASP.NET Core 指針

この指示は `**/*.cs` に一致する C# ファイルへ適用します。C# 14、ASP.NET Core 10、命名、フォーマット、Nullable 参照型、Entity Framework Core、認証と認可、検証、エラー処理、API ドキュメント、ロギング、テスト、パフォーマンス、デプロイに関する規約として authoritative です。プロジェクト固有の `.editorconfig`、ターゲット SDK、セキュリティ、アーキテクチャ、テスト規約がより厳しい場合はそれを優先します。

## C# スタイルと命名

- ターゲット SDK が対応している場合は最新の C#、現在は C# 14 の機能を使用します。
- 各関数には明確で簡潔なコメントを書きます。ただし明白な処理ではなく、設計判断や保守上の理由を説明します。
- コードレビューでは確信度の高い提案のみを行います。
- エッジケースに対応し、明確な例外処理を書きます。
- ライブラリや外部依存を追加する場合は用途と目的をコメントやドキュメントで明記します。

| 対象 | 規約 |
| --- | --- |
| コンポーネント名、メソッド名、公開メンバー | `PascalCase` |
| プライベートフィールド、ローカル変数 | `camelCase` |
| インターフェイス | `I` 接頭辞、例 `IUserService` |
| 公開 API | XML ドキュメントコメント、可能なら `<example>` と `<code>` |

## フォーマットと Nullable 参照型

- `.editorconfig` で定義されたフォーマットを適用します。
- ファイルスコープの namespace 宣言と 1 行の using ディレクティブを推奨します。
- `if`、`for`、`while`、`foreach`、`using`、`try` など任意のコードブロックでは、開始波括弧の前に改行を入れます。
- メソッドの最終 `return` 文は独立した行に配置します。
- 可能な限りパターンマッチングと switch 式を使用します。
- メンバー名参照には文字列リテラルではなく `nameof` を使用します。
- 変数は非 null で宣言し、エントリポイントで `null` を検査します。
- `== null` や `!= null` ではなく、常に `is null` または `is not null` を使用します。
- C# の null 注釈を信頼し、型システムが非 null を保証している値へ不要な null チェックを追加しません。

## プロジェクト構成とデータアクセス

適切な .NET テンプレートを選び、生成されるファイルとフォルダーの目的を説明できる構成にします。フィーチャーフォルダーやドメイン駆動設計（DDD）を使う場合は、モデル、サービス、データアクセス層の責務分離を明確にします。ASP.NET Core 10 の `Program.cs`、構成システム、環境別設定を一貫させます。

Entity Framework Core では開発および本番の選択肢として SQL Server、SQLite、In-Memory を説明し、必要な場面でのみリポジトリパターンを実装します。データベースマイグレーションとデータシーディングを用い、一般的なパフォーマンス問題を避ける効率的なクエリパターンを選びます。

## 認証、認可、検証、エラー処理

- JWT ベアラートークンを用いた認証を一貫して実装します。
- ASP.NET Core に関連する OAuth 2.0 と OpenID Connect の概念を説明します。
- ロールベースおよびポリシーベースの認可を使い分けます。
- Microsoft Entra ID（旧 Azure AD）との統合では、認証フローと構成を明確にします。
- コントローラーベース API と Minimal API の双方を一貫して保護します。
- データ注釈と FluentValidation を用いてモデル検証を実装します。
- 検証パイプラインと検証応答のカスタマイズを明確にします。
- ミドルウェアを用いたグローバル例外処理を実装します。
- API 全体で一貫したエラー応答を返し、標準化には Problem Details（RFC 9457）を使用します。

## API ドキュメント、ロギング、監視

- API バージョニング戦略を実装し、理由を説明します。
- Swagger / OpenAPI を適切なドキュメントとともに実装します。
- エンドポイント、パラメーター、応答、認証を文書化します。
- コントローラーベース API と Minimal API の双方でバージョニングを一貫させます。
- Serilog などを用いた構造化ロギングを実装します。
- ログレベルと使用場面を明確にします。
- Application Insights と統合してテレメトリを収集します。
- カスタムテレメトリと相関 ID を実装してリクエスト追跡を可能にします。
- API のパフォーマンス、エラー、利用パターンを監視します。

## テスト、パフォーマンス、デプロイ

- 重要な経路には必ずテストケースを含めます。
- 単体テスト、API エンドポイントの統合テスト、認証と認可ロジックのテストを作成します。
- テストでは `Act`、`Arrange`、`Assert` のコメントを書きません。
- 近傍ファイルの既存スタイル、テストメソッド名、大文字/小文字に合わせます。
- 依存関係をモックし、API 開発では TDD の原則を適用できるようにします。
- キャッシュ戦略はインメモリ、分散、レスポンスキャッシュから要件に合わせて選びます。
- 非同期プログラミング、大規模データセットのページング、フィルタリング、ソート、圧縮を適切に使います。
- API パフォーマンスを測定し、必要に応じてベンチマークします。
- .NET の組み込みコンテナーサポートを使う場合は `dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer` を使用します。
- 手動 Dockerfile と .NET コンテナー公開機能の違い、CI/CD、Azure App Service、Azure Container Apps、その他のホスティング、ヘルスチェック、Readiness Probe、環境固有構成を説明します。

## DevOps 補足

`DevOps` の文脈では、CI/CD、コンテナー化、Azure App Service、Azure Container Apps、ヘルスチェック、Readiness Probe、環境固有構成を一貫したデプロイ規約として扱います。

## Good / Bad Examples

以下の例は Nullable 参照型、`is null`、`nameof`、明確な例外処理を示します。

**Good:**

```csharp
public async Task<UserDto> GetUserAsync(string userId, CancellationToken cancellationToken)
{
    if (userId is null)
    {
        throw new ArgumentNullException(nameof(userId));
    }

    var user = await userRepository.FindAsync(userId, cancellationToken);
    return mapper.Map<UserDto>(user);
}
```

Why: `is null` と `nameof` を使い、非同期処理と例外の境界を明確にしています。

**Bad:**

```csharp
public async Task<UserDto> GetUserAsync(string userId)
{
    if (userId == null) throw new Exception("bad");
    return mapper.Map<UserDto>(await userRepository.FindAsync(userId));
}
```

Why: null 判定、例外型、キャンセルトークン、エラー文脈が不十分です。

## Conventions

| Rule | Rationale |
| --- | --- |
| 最新 SDK が対応する C# 14 と ASP.NET Core 10 の慣用構文を使う | 現代的な構文とフレームワーク機能で保守性を高める |
| `.editorconfig`、`PascalCase`、`camelCase`、`IUserService`、XML ドキュメントを守る | コードの一貫性と API 利用性を保つ |
| Nullable 参照型では `is null` / `is not null` と型注釈を信頼する | 不要な null チェックと曖昧な契約を減らす |
| EF Core、マイグレーション、シーディング、効率的なクエリを明示する | データアクセスの正確性と性能を守る |
| JWT、OAuth 2.0、OpenID Connect、Microsoft Entra ID、ロール/ポリシー認可を一貫して適用する | API 保護の抜け漏れを防ぐ |
| Problem Details（RFC 9457）、Swagger / OpenAPI、Serilog、Application Insights、相関 ID を使う | クライアント、運用、監視に一貫した情報を提供する |
| テスト、キャッシュ、非同期、ページング、コンテナー化、CI/CD を要件に合わせる | 品質、性能、デプロイ信頼性を保つ |

## Do / Do Not

| Do | Do not |
| --- | --- |
| `nameof` と XML ドキュメントコメントを公開 API に使う | 文字列リテラルでメンバー名を参照する |
| `is null` / `is not null` で null を判定する | `== null` / `!= null` を使う |
| コントローラー API と Minimal API を同じ認証認可方針で保護する | API 種別ごとに保護方針をばらつかせる |
| Problem Details（RFC 9457）で標準化されたエラーを返す | エンドポイントごとに異なるエラー形状を返す |
| 近傍テストのスタイルに合わせる | `Act`、`Arrange`、`Assert` コメントを追加する |
| `dotnet publish --os linux --arch x64 -p:PublishProfile=DefaultContainer` を適切なコンテナー化に使う | 要件を説明せず Dockerfile と組み込み公開を混在させる |

## Checklist Before Opening a PR

- [ ] C# 14 / ASP.NET Core 10 の使用可否をターゲット SDK とプロジェクト設定で確認した。
- [ ] 命名、フォーマット、波括弧、最終 `return`、`nameof`、XML ドキュメントが規約に従っている。
- [ ] Nullable 参照型、`is null`、エントリポイント検査が適切である。
- [ ] プロジェクト構成、DDD/フィーチャーフォルダー、モデル、サービス、データアクセスの責務が明確である。
- [ ] EF Core、マイグレーション、シーディング、クエリ性能が確認されている。
- [ ] 認証、認可、検証、グローバル例外処理、Problem Details（RFC 9457）が一貫している。
- [ ] Swagger / OpenAPI、ログ、Application Insights、相関 ID、監視の更新が必要に応じて含まれている。
- [ ] 単体テスト、統合テスト、認証認可テストが近傍スタイルに従い、AAA コメントを含まない。
- [ ] キャッシュ、非同期、ページング、フィルタリング、ソート、圧縮、ベンチマーク、デプロイ設定が要件に合う。
